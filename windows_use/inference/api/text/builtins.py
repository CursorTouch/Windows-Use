# Lazy registry entries: each provider API is referenced by a "module:ClassName"
# path so its SDK (anthropic, openai, google.genai, mistralai, ...) is only
# imported when that provider is actually used. Loading every SDK at startup
# previously cost ~1.5s on cold start.
LLM_APIS: list[tuple[str, str]] = [
    ("openai_responses",       "operator_use.inference.api.text.openai_responses:OpenAIResponsesAPI"),
    ("openai_completions",     "operator_use.inference.api.text.openai_completions:OpenAICompletionsAPI"),
    ("openai_codex_responses", "operator_use.inference.api.text.openai_codex_responses:OpenAICodexResponsesAPI"),
    ("anthropic_messages",     "operator_use.inference.api.text.anthropic_messages:AnthropicMessagesAPI"),
    ("anthropic_claude_code",  "operator_use.inference.api.text.anthropic_claude_code:AnthropicClaudeCodeAPI"),
    ("github_copilot_chat",    "operator_use.inference.api.text.github_copilot_chat:GitHubCopilotChatAPI"),
    ("gemini_generate",        "operator_use.inference.api.text.gemini_generate:GeminiGenerateAPI"),
    ("mistral_chat",           "operator_use.inference.api.text.mistral_chat:MistralChatAPI"),
    ("ollama_chat",            "operator_use.inference.api.text.ollama_chat:OllamaChatAPI"),
    ("google_antigravity",     "operator_use.inference.api.text.google_antigravity:GoogleAntigravityAPI"),
]

# Backward-compat alias
APIS = LLM_APIS
