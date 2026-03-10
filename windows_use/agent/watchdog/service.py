"""
Unified WatchDog Service for monitoring UI Automation events.
Allows single instantiation to handle multiple monitors (Focus, Structure) safely in one STA thread.
"""
from windows_use.uia.core import _AutomationClient
from windows_use.uia.enums import TreeScope
from threading import Thread, Event
import comtypes.client
import comtypes
import logging
import weakref

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class WatchDog:
    def __init__(self):
        self.is_running = Event()
        self._config_changed = Event()
        self.thread = None
        self.uia = None

        # Callbacks
        self._focus_callback = None
        self._structure_callback = None
        self._structure_element = None
        self._property_callback = None
        self._property_element = None
        self._property_ids = None
        
        # Internal state for tracking active handlers
        self._focus_handler = None
        self._structure_handler = None
        self._active_structure_element = None
        self._property_handler = None
        self._active_property_element = None
        self._active_property_ids = None

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def start(self):
        """Start the watchdog service thread."""
        if self.is_running.is_set():
            return
        self.is_running.set()
        self.thread = Thread(target=self._run, name="WatchDogThread")
        self.thread.daemon = True 
        self.thread.start()

    def stop(self):
        """Stop the watchdog service thread."""
        if not self.is_running.is_set():
            return
        self.is_running.clear()
        self._config_changed.set()
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=2.0)

    def set_focus_callback(self, callback):
        """Set the callback for focus changes. Pass None to disable."""
        self._focus_callback = callback
        self._config_changed.set()

    def set_structure_callback(self, callback, element=None):
        """Set the callback for structure changes. Pass None to disable.
        Optionally specify an element to watch (defaults to RootElement)."""
        self._structure_callback = callback
        self._structure_element = element
        self._config_changed.set()

    def set_property_callback(self, callback, element=None, property_ids=None):
        """Set the callback for property changes. Pass None to disable.
        Optionally specify an element to watch (defaults to RootElement) 
        and a list of property IDs to monitor."""
        self._property_callback = callback
        self._property_element = element
        self._property_ids = property_ids
        self._config_changed.set()

    def _sync_handlers(self, FocusChangedEventHandler, StructureChangedEventHandler, PropertyChangedEventHandler):
        """Reconcile desired callback config with active COM handlers."""
        # --- Focus Monitoring ---
        if self._focus_callback and not self._focus_handler:
            try:
                self._focus_handler = FocusChangedEventHandler(self)
                self.uia.AddFocusChangedEventHandler(None, self._focus_handler)
            except Exception as e:
                logger.debug(f"Failed to add focus handler: {e}")
        elif not self._focus_callback and self._focus_handler:
            try:
                self.uia.RemoveFocusChangedEventHandler(self._focus_handler)
            except Exception as e:
                logger.debug(f"Failed to remove focus handler: {e}")
            self._focus_handler = None

        # --- Structure Monitoring ---
        config_changed = (self._structure_element != self._active_structure_element)
        should_be_active = (self._structure_callback is not None)
        is_active = (self._structure_handler is not None)

        if is_active and (not should_be_active or config_changed):
            try:
                target = self._active_structure_element if self._active_structure_element else self.uia.GetRootElement()
                self.uia.RemoveStructureChangedEventHandler(target, self._structure_handler)
            except Exception as e:
                logger.debug(f"Failed to remove structure handler: {e}")
            self._structure_handler = None
            self._active_structure_element = None
            is_active = False

        if should_be_active and not is_active:
            try:
                target = self._structure_element if self._structure_element else self.uia.GetRootElement()
                scope = TreeScope.TreeScope_Subtree
                self._structure_handler = StructureChangedEventHandler(self)
                self.uia.AddStructureChangedEventHandler(target, scope, None, self._structure_handler)
                self._active_structure_element = target
            except Exception as e:
                logger.debug(f"Failed to add structure handler: {e}")

        # --- Property Monitoring ---
        config_changed = (self._property_element != self._active_property_element) or \
                       (self._property_ids != self._active_property_ids)
        should_be_active = (self._property_callback is not None)
        is_active = (self._property_handler is not None)

        if is_active and (not should_be_active or config_changed):
            try:
                target = self._active_property_element if self._active_property_element else self.uia.GetRootElement()
                self.uia.RemovePropertyChangedEventHandler(target, self._property_handler)
            except Exception as e:
                logger.error(f"Failed to remove property handler: {e}")
            self._property_handler = None
            self._active_property_element = None
            self._active_property_ids = None
            is_active = False

        if should_be_active and not is_active:
            try:
                target = self._property_element if self._property_element else self.uia.GetRootElement()
                scope = TreeScope.TreeScope_Subtree
                # 30005: Name, 30045: Value, 30093: LegacyIAccessibleVal, 30128: ToggleState
                p_ids = self._property_ids if self._property_ids else [30005, 30045, 30093, 30128]
                self._property_handler = PropertyChangedEventHandler(self)
                self.uia.AddPropertyChangedEventHandler(target, scope, None, self._property_handler, p_ids)
                self._active_property_element = target
                self._active_property_ids = p_ids
            except Exception as e:
                logger.error(f"Failed to add property handler: {e}")

    def _run(self):
        """Main event loop running in a dedicated STA thread."""
        comtypes.CoInitialize()
        try:
            from .event_handlers import (
                FocusChangedEventHandler,
                StructureChangedEventHandler,
                PropertyChangedEventHandler
            )
            # Initialize UIA inside the thread
            uia_client = _AutomationClient.instance()
            self.uia = uia_client.IUIAutomation

            while self.is_running.is_set():
                if self._config_changed.is_set():
                    self._config_changed.clear()
                    self._sync_handlers(FocusChangedEventHandler, StructureChangedEventHandler, PropertyChangedEventHandler)

                comtypes.client.PumpEvents(0.1)

        except Exception as e:
            logger.error(f"WatchDogService died: {e}")
        finally:
            # Cleanup handlers on exit
            if self.uia:
                if self._focus_handler:
                    try: 
                        self.uia.RemoveFocusChangedEventHandler(self._focus_handler)
                    except Exception:
                        pass
                    self._focus_handler = None
                
                if self._structure_handler:
                    try:
                        target = self._active_structure_element if self._active_structure_element else self.uia.GetRootElement()
                        self.uia.RemoveStructureChangedEventHandler(target, self._structure_handler)
                    except Exception:
                        pass
                    self._structure_handler = None
                    self._active_structure_element = None

                if self._property_handler:
                    try:
                        target = self._active_property_element if self._active_property_element else self.uia.GetRootElement()
                        self.uia.RemovePropertyChangedEventHandler(target, self._property_handler)
                    except Exception:
                        pass
                    self._property_handler = None
                    self._active_property_element = None
                    self._active_property_ids = None
            
            comtypes.CoUninitialize()
