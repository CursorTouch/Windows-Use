from windows_use.uia.core import _AutomationClient
import comtypes
import weakref

# Get UIA Interface for COM definitions
uia_client = _AutomationClient.instance()
UIA = uia_client.UIAutomationCore

class FocusChangedEventHandler(comtypes.COMObject):
    _com_interfaces_ = [UIA.IUIAutomationFocusChangedEventHandler]

    def __init__(self, parent):
        self._parent = weakref.ref(parent)
        super(FocusChangedEventHandler, self).__init__()

    def HandleFocusChangedEvent(self, sender):
        try:
            parent = self._parent()
            if parent and parent._focus_callback:
                parent._focus_callback(sender)
        except Exception as e:
            print(f"Error in focus callback: {e}")
        return 0 # S_OK

class StructureChangedEventHandler(comtypes.COMObject):
    _com_interfaces_ = [UIA.IUIAutomationStructureChangedEventHandler]

    def __init__(self, parent):
        self._parent = weakref.ref(parent)
        super(StructureChangedEventHandler, self).__init__()

    def HandleStructureChangedEvent(self, sender, changeType, runtimeId):
        try:
            parent = self._parent()
            if parent and parent._structure_callback:
                parent._structure_callback(sender, changeType, runtimeId)
        except Exception as e:
            print(f"Error in structure callback: {e}")
        return 0 # S_OK

class PropertyChangedEventHandler(comtypes.COMObject):
    _com_interfaces_ = [UIA.IUIAutomationPropertyChangedEventHandler]

    def __init__(self, parent):
        self._parent = weakref.ref(parent)
        super(PropertyChangedEventHandler, self).__init__()

    def HandlePropertyChangedEvent(self, sender, propertyId, newValue):
        try:
            parent = self._parent()
            if parent and parent._property_callback:
                parent._property_callback(sender, propertyId, newValue)
        except Exception as e:
            print(f"Error in property callback: {e}")
        return 0 # S_OK
