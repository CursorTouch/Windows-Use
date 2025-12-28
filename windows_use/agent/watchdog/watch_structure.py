from windows_use.uia.enums import StructureChangeType
from windows_use.uia.core import _AutomationClient
from windows_use.uia import Control
from threading import Thread, Event
from time import sleep
import comtypes.client
import comtypes

uia_client = _AutomationClient.instance()
UIA = uia_client.UIAutomationCore

class StructureChangedEventHandler(comtypes.COMObject):
    _com_interfaces_ = [UIA.IUIAutomationStructureChangedEventHandler]

    def __init__(self, callback):
        self.callback = callback
        super(StructureChangedEventHandler, self).__init__()

    def HandleStructureChangedEvent(self, sender, changeType, runtimeId):
        try:
            if self.callback:
                self.callback(sender, changeType, runtimeId)
        except Exception:
            pass
        return 0 # S_OK

class WatchStructure:
    def __init__(self, element=None, callback=None):
        self.is_running = Event()
        self.uia = uia_client.IUIAutomation
        self.thread = None
        self.element = element 
        self.callback = callback

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def structure_changed_func(self):
        def default_callback(sender, changeType, runtimeId):
            try:
                msg = f"Structure Changed: Type={changeType}"
                
                try:
                    control = Control.CreateControlFromElement(sender)
                    if control:
                        name = control.Name
                        control_type_name = control.ControlTypeName
                        msg += f" [Element: '{name}' ({control_type_name})]"
                except Exception:
                    pass

                match changeType:
                    case StructureChangeType.StructureChangeType_ChildAdded:
                        msg += " (ChildAdded)"
                    case StructureChangeType.StructureChangeType_ChildRemoved:
                        msg += " (ChildRemoved)"
                    case StructureChangeType.StructureChangeType_ChildrenInvalidated:
                        msg += " (ChildrenInvalidated)"
                    case StructureChangeType.StructureChangeType_ChildrenBulkAdded:
                        msg += " (ChildrenBulkAdded)"
                    case StructureChangeType.StructureChangeType_ChildrenBulkRemoved:
                        msg += " (ChildrenBulkRemoved)"
                    case StructureChangeType.StructureChangeType_ChildrenReordered:
                        msg += " (ChildrenReordered)"
                
                print(msg, flush=True)
            except Exception:
                pass

        callback = self.callback if self.callback else default_callback

        structure_handler = StructureChangedEventHandler(callback)

        try:
            comtypes.CoInitialize()
            target_element = self.element
            if target_element is None:
                target_element = self.uia.GetRootElement()

            # Scope: TreeScope_Subtree
            try:
                scope = UIA.TreeScope_Subtree
            except AttributeError:
                scope = 7 # Fallback
            
            self.uia.AddStructureChangedEventHandler(target_element, scope, None, structure_handler)
            
            try:
                while self.is_running.is_set():
                    # Pump messages for STA COM events
                    comtypes.client.PumpEvents(0.1)
            finally:
                # Always attempt to remove the handler
                try:
                    uia.RemoveStructureChangedEventHandler(target_element, structure_handler)
                except Exception as e:
                    print(f"Error removing structure handler: {e}", flush=True)

        except Exception as e:
            print(f"Error in WatchStructure loop: {e}", flush=True)
        finally:
            comtypes.CoUninitialize()

    def start(self):
        if self.is_running.is_set():
            return

        self.is_running.set()
        self.thread = Thread(target=self.structure_changed_func, name='WatchStructureThread')
        self.thread.start()

    def stop(self):
        if not self.is_running.is_set():
            return

        self.is_running.clear()
        
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=2.0)

if __name__ == "__main__":
    watcher = WatchStructure()
    try:
        watcher.start()
        print("Watching structure changes. Press Ctrl+C to stop.", flush=True)
        while True:
            sleep(1)
    except KeyboardInterrupt:
        print("Stopping...", flush=True)
        watcher.stop()
