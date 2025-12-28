from windows_use.uia.core import _AutomationClient
from windows_use.uia import Control
from threading import Thread, Event
from time import sleep
import comtypes.client
import comtypes

uia_client = _AutomationClient.instance()
UIA = uia_client.UIAutomationCore

class FocusChangedEventHandler(comtypes.COMObject):
    _com_interfaces_ = [UIA.IUIAutomationFocusChangedEventHandler]

    def __init__(self, callback):
        self.callback = callback
        super(FocusChangedEventHandler, self).__init__()

    def HandleFocusChangedEvent(self, sender):
        try:
            if self.callback:
                self.callback(sender)
        except Exception as e:
            # Prevent exceptions from crashing the COM callback
            pass
        return 0 # S_OK

class WatchFocus:
    def __init__(self, callback=None):
        self.is_running = Event()
        self.focus_thread = None
        # We access the UIA object specifically within the thread if needed,
        # but using the shared interface pointer is generally fine if MTA.
        self.uia = uia_client.IUIAutomation
        self.callback = callback

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def focus_changed_func(self):
        # Default callback if none provided
        def default_callback(sender):
            try:
                # Basic logging
                element = Control.CreateControlFromElement(sender)
                print(f"Focus Changed: '{element.Name}' ({element.ControlTypeName})", flush=True)
            except Exception:
                pass

        callback = self.callback if self.callback else default_callback

        # Create the handler
        focus_handler = FocusChangedEventHandler(callback)
        try:
            comtypes.CoInitialize() 
            self.uia.AddFocusChangedEventHandler(None, focus_handler)
            
            while self.is_running.is_set():
                # Pump messages to allow COM events to be processed
                comtypes.client.PumpEvents(0.1)
                
        except Exception as e:
            print(f"Error in WatchFocus loop: {e}", flush=True)
        finally:
            try:
                self.uia.RemoveFocusChangedEventHandler(focus_handler)
            except Exception as e:
                print(f"Error removing focus handler: {e}", flush=True)
            
            comtypes.CoUninitialize()

    def start(self):
        if self.is_running.is_set():
            return

        self.is_running.set()
        self.focus_thread = Thread(target=self.focus_changed_func, name='WatchFocusThread')
        self.focus_thread.start()

    def stop(self):
        if not self.is_running.is_set():
            return

        self.is_running.clear()
        
        if self.focus_thread and self.focus_thread.is_alive():
            self.focus_thread.join(timeout=2.0)

if __name__ == "__main__":
    watcher = WatchFocus()
    try:
        watcher.start()
        print("Watching focus changes. Press Ctrl+C to stop.", flush=True)
        while True:
            sleep(1)
    except KeyboardInterrupt:
        print("Stopping...", flush=True)
        watcher.stop()
