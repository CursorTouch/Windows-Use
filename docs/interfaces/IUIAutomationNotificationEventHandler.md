# IUIAutomationNotificationEventHandler

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nn-uiautomationclient-iuiautomationnotificationeventhandler)

# IUIAutomationNotificationEventHandler interface (uiautomationclient.h)

Exposes a method to handle Microsoft UI Automation notification events.

## Inheritance

The **IUIAutomationNotificationEventHandler** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **IUIAutomationNotificationEventHandler** also has these types of members:

## Methods

The **IUIAutomationNotificationEventHandler** interface has these methods.

|  |
| --- |
| [IUIAutomationNotificationEventHandler::HandleNotificationEvent](nf-uiautomationclient-iuiautomationnotificationeventhandler-handlenotificationevent)   Handles a Microsoft UI Automation notification event. |

## Remarks

This interface is implemented by the application to handle events that it has subscribed to by calling [AddNotificationEventHandler](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomation5-addnotificationeventhandler).

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 10, version 1709 [desktop apps only] |
| **Minimum supported server** | Windows Server 2016 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[Event Handling Interfaces for Clients](/en-us/windows/desktop/WinAuto/uiauto-client-eventhandlinginterfaces)

---
