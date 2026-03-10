# IUIAutomation2

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nn-uiautomationclient-iuiautomation2)

# IUIAutomation2 interface (uiautomationclient.h)

Extends the [IUIAutomation](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomation) interface to expose additional methods for controlling Microsoft UI Automation functionality.

## Inheritance

The **IUIAutomation2** interface inherits from the IUIAutomation interface.

## Methods

The **IUIAutomation2** interface has these methods.

|  |
| --- |
| [IUIAutomation2::get\_AutoSetFocus](nf-uiautomationclient-iuiautomation2-get_autosetfocus)   Specifies whether calls to UI Automation control pattern methods automatically set focus to the target element. (Get) |
| [IUIAutomation2::get\_ConnectionTimeout](nf-uiautomationclient-iuiautomation2-get_connectiontimeout)   Specifies the length of time that UI Automation will wait for a provider to respond to a client request for an automation element. (Get) |
| [IUIAutomation2::get\_TransactionTimeout](nf-uiautomationclient-iuiautomation2-get_transactiontimeout)   Specifies the length of time that UI Automation will wait for a provider to respond to a client request for information about an automation element. (Get) |
| [IUIAutomation2::put\_AutoSetFocus](nf-uiautomationclient-iuiautomation2-put_autosetfocus)   Specifies whether calls to UI Automation control pattern methods automatically set focus to the target element. (Put) |
| [IUIAutomation2::put\_ConnectionTimeout](nf-uiautomationclient-iuiautomation2-put_connectiontimeout)   Specifies the length of time that UI Automation will wait for a provider to respond to a client request for an automation element. (Put) |
| [IUIAutomation2::put\_TransactionTimeout](nf-uiautomationclient-iuiautomation2-put_transactiontimeout)   Specifies the length of time that UI Automation will wait for a provider to respond to a client request for information about an automation element. (Put) |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 8 [desktop apps only] |
| **Minimum supported server** | Windows Server 2012 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[IUIAutomation](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomation)

[UI Automation Element Interfaces for Clients](/en-us/windows/desktop/WinAuto/uiauto-entry-uiautoclientinterfaces)

---
