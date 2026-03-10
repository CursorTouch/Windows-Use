# IUIAutomationFocusChangedEventHandler

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nn-uiautomationclient-iuiautomationfocuschangedeventhandler)

# IUIAutomationFocusChangedEventHandler interface (uiautomationclient.h)

Exposes a method to handle events that are raised when the keyboard focus moves to another UI Automation element.

## Inheritance

The **IUIAutomationFocusChangedEventHandler** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **IUIAutomationFocusChangedEventHandler** also has these types of members:

## Methods

The **IUIAutomationFocusChangedEventHandler** interface has these methods.

|  |
| --- |
| [IUIAutomationFocusChangedEventHandler::HandleFocusChangedEvent](nf-uiautomationclient-iuiautomationfocuschangedeventhandler-handlefocuschangedevent)   Handles the event raised when the keyboard focus moves to a different UI Automation element. |

## Remarks

This interface is implemented by the application to handle events that were subscribed to by using [AddFocusChangedEventHandler](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomation-addfocuschangedeventhandler)

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[Event Handling Interfaces for Clients](/en-us/windows/desktop/WinAuto/uiauto-client-eventhandlinginterfaces)

---
