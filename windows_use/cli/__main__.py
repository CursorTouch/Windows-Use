"""CLI interface for Windows-Use, built with Typer."""

import logging
import os
import re
import sys
import time
import threading

from dotenv import load_dotenv

import typer

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion

from windows_use.cli.config import get_active_config
from windows_use.cli.registry import PROVIDER_DISPLAY, get_provider_display

load_dotenv()


# Dot animation: filled dot moves left to right •○○ -> ○•○ -> ○○•
_DOT_FRAMES = "•○○", "○•○", "○○•"


def _animate_circles(line: str, stop_event: threading.Event) -> None:
    """Show dots moving left-to-right (e.g. > •○○ Transcribing...)."""
    i = 0
    while not stop_event.is_set():
        dots = _DOT_FRAMES[i % 3]
        sys.stdout.write(f"\r> {dots} {line}")
        sys.stdout.flush()
        time.sleep(0.4)
        i += 1
    # Clear the line: "> •○○ " + line content
    line_len = 6 + len(line)
    sys.stdout.write("\r" + " " * line_len + "\r")
    sys.stdout.flush()


def _overwrite_line(text: str) -> None:
    """Overwrite current line with text (no newline)."""
    sys.stdout.write(f"\r\033[K{text}")
    sys.stdout.flush()


def _strip_markdown(text: str) -> str:
    """Strip markdown formatting to plain text for TTS."""
    if not text:
        return ""
    t = text
    t = re.sub(r"\*\*(.+?)\*\*", r"\1", t)
    t = re.sub(r"\*(.+?)\*", r"\1", t)
    t = re.sub(r"__(.+?)__", r"\1", t)
    t = re.sub(r"_(.+?)_", r"\1", t)
    t = re.sub(r"^#{1,6}\s*", "", t, flags=re.MULTILINE)
    t = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", t)
    t = re.sub(r"!\[([^\]]*)\]\([^\)]+\)", r"\1", t)
    t = re.sub(r"```[\s\S]*?```", "", t)
    t = re.sub(r"`([^`]+)`", r"\1", t)
    t = re.sub(r"^\s*[-*+]\s+", "", t, flags=re.MULTILINE)
    t = re.sub(r"^\s*\d+\.\s+", "", t, flags=re.MULTILINE)
    return re.sub(r"\n{3,}", "\n\n", t).strip()

app = typer.Typer(
    name="windows-use",
    help="Windows-Use: Computer-Use for Windows OS.",
    invoke_without_command=True,
)

def _version() -> str:
    try:
        from importlib.metadata import version
        return version("windows-use")
    except Exception:
        return "0.0.0"


def _normalize_provider(name: str) -> str:
    """Normalize provider name to key (e.g. Groq -> groq)."""
    key = name.lower().replace(" ", "_")
    return key if key in PROVIDER_DISPLAY else name


def _resolve_provider_model(model_opt: str | None, provider_opt: str | None) -> tuple[str, str]:
    """Resolve provider and model from config or CLI options."""
    from windows_use.cli.setup import run_setup

    # Skip setup if both provider and model provided via CLI
    if provider_opt and model_opt:
        return _normalize_provider(provider_opt), model_opt

    active = get_active_config()
    if not active:
        try:
            run_setup()
            active = get_active_config()
        except KeyboardInterrupt:
            raise typer.Exit(130)

    provider = provider_opt or active.get("provider")
    model = model_opt or active.get("llm")
    return provider, model


@app.callback()
def _callback(
    ctx: typer.Context,
    version_flag: bool = typer.Option(
        False,
        "--version",
        "-v",
        help="Show version and exit.",
    ),
    model: str | None = typer.Option(
        None,
        "--model",
        "-m",
        help="LLM model ID to use (overrides config). Supports both predefined and custom models.",
    ),
    provider: str | None = typer.Option(
        None,
        "--provider",
        "-p",
        help="LLM provider to use (overrides config).",
    ),
    max_steps: int = typer.Option(
        200,
        "--max-steps",
        help="Maximum agent steps per task.",
    ),
    debug: bool = typer.Option(
        False,
        "--debug",
        "-d",
        help="Enable debug logging (e.g. [STT]/[TTS] messages).",
    ),
) -> None:
    """Interactive CLI: accept tasks, execute them, show intermediates, wait for next."""
    if debug:
        logging.getLogger("windows_use.speech.service").setLevel(logging.DEBUG)
    if version_flag:
        typer.echo("Windows-Use ", nl=False)
        typer.secho(f"v{_version()}", fg="green", nl=False)
        typer.echo()
        raise typer.Exit()

    if ctx.invoked_subcommand is not None:
        return

    provider_key, model_id = _resolve_provider_model(model, provider)
    _run_interactive(provider=provider_key, model=model_id, max_steps=max_steps, debug=debug)


# Commands available when typing \ (backslash): (command, description)
_CLI_COMMANDS = (
    ("\\quit", "Exit the session"),
    ("\\llm", "Switch provider or model"),
    ("\\key", "Change API key for a provider"),
    ("\\speech", "Configure Speech-to-Text / Text-to-Speech"),
    ("\\voice", "Use voice input (Speech-to-Text)"),
    ("\\clear", "Clear the screen"),
)


class _CommandCompleter(Completer):
    """Completer for \\ commands. Filters suggestions as user types after \\."""

    def get_completions(self, document, complete_event):
        text = document.text.strip().lower()
        if not text.startswith("\\"):
            return
        prefix = text
        for cmd, desc in _CLI_COMMANDS:
            if cmd.lower().startswith(prefix):
                yield Completion(cmd, start_position=-len(document.text), display_meta=desc)


def _prompt_task(default: str = "") -> str:
    r"""Read input with \ command autocomplete. Use default to pre-fill (e.g. after voice transcribe)."""
    session = PromptSession(
        completer=_CommandCompleter(),
        complete_while_typing=True,
    )
    return session.prompt("> ", default=default).strip()


def _clear_screen() -> None:
    """Clear the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")


def _run_interactive(provider: str, model: str, max_steps: int, debug: bool = False) -> None:
    """Run the interactive task loop."""
    from windows_use.cli.setup import create_llm, run_llm_switch, run_speech_setup
    from windows_use.cli.setup import create_stt_provider, create_tts_provider
    from windows_use.cli.config import get_active_config
    from windows_use.agent import Agent, Browser
    from windows_use.cli.subscriber import CLIEventSubscriber

    agent = None
    # Get base_url from config if available
    active_config = get_active_config()
    base_url = active_config.get("base_url") if active_config else None
    llm = create_llm(provider, model, base_url=base_url)
    provider_display = get_provider_display(provider)

    # Resolve STT/TTS (lazy - may fail if pyaudio not installed)
    stt_provider = create_stt_provider()
    tts_provider = create_tts_provider()
    stt_instance = None
    tts_instance = None
    if stt_provider:
        try:
            from windows_use.speech import STT
            stt_instance = STT(provider=stt_provider, verbose=False)
        except ImportError:
            stt_provider = None
    if tts_provider:
        try:
            from windows_use.speech import TTS
            tts_instance = TTS(provider=tts_provider, verbose=False)
        except ImportError:
            tts_provider = None

    _clear_screen()

    typer.echo("Windows-Use ", nl=False)
    typer.secho(f"v{_version()}", fg="green", nl=False)
    typer.echo(f" | {provider_display}: {model}")
    hint = "Type \\quit, \\exit, or \\q to leave."
    if stt_instance:
        hint += " \\voice for voice input."
    typer.secho(hint + "\n", fg="bright_black")

    def _make_tts_callback():
        def cb(content: str) -> None:
            if not tts_instance:
                return
            try:
                typer.echo()
                # Synthesizing: text → model → audio
                synth_stop = threading.Event()
                synth_anim = threading.Thread(
                    target=_animate_circles,
                    args=("Synthesizing...", synth_stop),
                    daemon=True,
                )
                synth_anim.start()
                try:
                    tts_instance.generate_audio(_strip_markdown(content))
                finally:
                    synth_stop.set()
                    synth_anim.join(timeout=0.5)
                # Speaking: playing the audio
                speak_stop = threading.Event()
                speak_anim = threading.Thread(
                    target=_animate_circles,
                    args=("Speaking...", speak_stop),
                    daemon=True,
                )
                speak_anim.start()
                try:
                    tts_instance.play_audio()
                finally:
                    speak_stop.set()
                    speak_anim.join(timeout=0.5)
            except Exception as e:
                typer.secho(f"TTS playback failed: {e}", fg="yellow")

        return cb if tts_instance else None

    while True:
        try:
            task = _prompt_task()
        except (EOFError, KeyboardInterrupt):
            break

        if not task:
            continue
        if task.lower() in ("quit", "exit", "q", "\\quit", "\\exit", "\\q"):
            break

        if task.lower() in ("clear", "\\clear"):
            _clear_screen()
            typer.echo("Windows-Use ", nl=False)
            typer.secho(f"v{_version()}", fg="green", nl=False)
            typer.echo(f" | {provider_display} | {model}")
            typer.secho("Type \\quit, \\exit, or \\q to leave.\n", fg="bright_black")
            continue

        if task.lower() in ("key", "\\key"):
            try:
                from windows_use.cli.setup import run_key_change
                if run_key_change():
                    active_config = get_active_config()
                    base_url = active_config.get("base_url") if active_config else None
                    llm = create_llm(provider, model, base_url=base_url)
                    agent = Agent(
                        llm=llm,
                        browser=Browser.EDGE,
                        auto_minimize=False,
                        log_to_console=False,
                        log_to_file=False,
                        max_steps=max_steps,
                        event_subscriber=CLIEventSubscriber(tts_callback=_make_tts_callback()),
                    )
                    typer.secho("API key updated and applied.", fg="green")
                else:
                    typer.secho("No providers with API keys configured. Use \\llm first.", fg="yellow")
            except KeyboardInterrupt:
                pass
            continue

        if task.lower() in ("speech", "\\speech"):
            try:
                from windows_use.cli.setup import run_speech_setup, create_stt_provider, create_tts_provider
                run_speech_setup(initial_setup=False)
                stt_provider = create_stt_provider()
                tts_provider = create_tts_provider()
                if stt_provider:
                    try:
                        from windows_use.speech import STT
                        stt_instance = STT(provider=stt_provider, verbose=False)
                    except ImportError:
                        stt_instance = None
                        typer.secho("Install pyaudio for voice input: uv add windows-use[speech]", fg="yellow")
                else:
                    stt_instance = None
                if tts_provider:
                    try:
                        from windows_use.speech import TTS
                        tts_instance = TTS(provider=tts_provider, verbose=False)
                    except ImportError:
                        tts_instance = None
                        typer.secho("Install pyaudio for spoken responses: uv add windows-use[speech]", fg="yellow")
                else:
                    tts_instance = None
                # Recreate agent so it picks up new TTS callback
                if agent is not None:
                    agent = Agent(
                        llm=llm,
                        browser=Browser.EDGE,
                        auto_minimize=False,
                        log_to_console=False,
                        log_to_file=False,
                        max_steps=max_steps,
                        event_subscriber=CLIEventSubscriber(tts_callback=_make_tts_callback()),
                    )
            except KeyboardInterrupt:
                pass
            continue

        if task.lower() in ("voice", "\\voice"):
            if stt_instance is None:
                typer.secho("Speech-to-Text not configured. Use \\speech to set it up.", fg="yellow")
                continue
            try:
                # Clear the "> \voice" line and show recording on same line
                sys.stdout.write("\033[A\r\033[K")  # up one line, start, clear
                sys.stdout.flush()
                stop_event = threading.Event()
                anim = threading.Thread(
                    target=_animate_circles,
                    args=("Listening... (press enter to stop)", stop_event),
                    daemon=True,
                )
                stt_instance.start_recording()
                anim.start()
                try:
                    input()
                except EOFError:
                    pass
                stop_event.set()
                anim.join(timeout=0.5)
                stt_instance.stop_recording()
                # Go back up (input() echoed newline) and show animated Transcribing...
                sys.stdout.write("\033[A")
                sys.stdout.flush()
                transcribe_stop = threading.Event()
                transcribe_anim = threading.Thread(
                    target=_animate_circles,
                    args=("Transcribing...", transcribe_stop),
                    daemon=True,
                )
                transcribe_anim.start()
                task = stt_instance.process_audio().strip()
                transcribe_stop.set()
                transcribe_anim.join(timeout=0.5)
                stt_instance.close()
                if not task:
                    _overwrite_line("> ")
                    typer.secho("No speech detected.", fg="yellow")
                    continue
                # Clear "> Transcribing..." so prompt renders cleanly (avoids "> Transcribing...> Hello.")
                _overwrite_line("")
                sys.stdout.flush()
                task = _prompt_task(default=task)
                if not task:
                    continue
            except ImportError as e:
                typer.secho(f"Voice input requires pyaudio: uv add windows-use[speech]", fg="yellow")
                continue
            except Exception as e:
                typer.secho(f"Voice input failed: {e}", fg="red")
                continue

        if task.lower() in ("llm", "\\llm"):
            try:
                result = run_llm_switch()
            except KeyboardInterrupt:
                continue
            if result is None:
                continue
            provider, model = result
            active_config = get_active_config()
            base_url = active_config.get("base_url") if active_config else None
            llm = create_llm(provider, model, base_url=base_url)
            provider_display = get_provider_display(provider)

            agent = Agent(
                llm=llm,
                browser=Browser.EDGE,
                auto_minimize=False,
                log_to_console=False,
                log_to_file=False,
                max_steps=max_steps,
                event_subscriber=CLIEventSubscriber(tts_callback=_make_tts_callback()),
            )
            _clear_screen()
            typer.echo("Windows-Use ", nl=False)
            typer.secho(f"v{_version()}", fg="green", nl=False)
            typer.echo(f" | {provider_display} | {model}")
            typer.secho("Type \\quit, \\exit, or \\q to leave.\n", fg="bright_black")
            continue

        if agent is None:
            event_subscriber = CLIEventSubscriber(tts_callback=_make_tts_callback())
            agent = Agent(
                llm=llm,
                browser=Browser.EDGE,
                auto_minimize=False,
                log_to_console=False,
                log_to_file=False,
                max_steps=max_steps,
                event_subscriber=event_subscriber,
            )
        import asyncio
        result = asyncio.run(agent.ainvoke(task=task))

def main() -> None:
    """Entry point for the console script."""
    app()


if __name__ == "__main__":
    app()
