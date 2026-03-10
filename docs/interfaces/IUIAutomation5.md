# IUIAutomation5

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nn-uiautomationclient-iuiautomation5)

# IUIAutomation5 interface (uiautomationclient.h)

Extends the [IUIAutomation4](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomation4) interface to expose additional methods for controlling Microsoft UI Automation functionality.

## Inheritance

The **IUIAutomation5** interface inherits from [IUIAutomation4](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomation4). **IUIAutomation5** also has these types of members:

## Methods

The **IUIAutomation5** interface has these methods.

|  |
| --- |
| [IUIAutomation5::AddNotificationEventHandler](nf-uiautomationclient-iuiautomation5-addnotificationeventhandler)   Registers a method that handles notification events.Note  Before implementing an event handler, you should be familiar with the threading issues described in Understanding Threading Issues. |
| [IUIAutomation5::RemoveNotificationEventHandler](nf-uiautomationclient-iuiautomation5-removenotificationeventhandler)   Removes a notification event handler. |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 10, version 1607 [desktop apps only] |
| **Minimum supported server** | Windows Server, version 1709 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[IUIAutomation4](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomation4)

[UI Automation Element Interfaces for Clients](/en-us/windows/desktop/WinAuto/uiauto-entry-uiautoclientinterfaces)

---
