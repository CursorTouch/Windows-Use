# IUIAutomation4

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nn-uiautomationclient-iuiautomation4)

# IUIAutomation4 interface (uiautomationclient.h)

Extends the [IUIAutomation3](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomation3) interface to expose additional methods for controlling Microsoft UI Automation functionality.

## Inheritance

The **IUIAutomation4** interface inherits from [IUIAutomation3](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomation3). **IUIAutomation4** also has these types of members:

## Methods

The **IUIAutomation4** interface has these methods.

|  |
| --- |
| [IUIAutomation4::AddChangesEventHandler](nf-uiautomationclient-iuiautomation4-addchangeseventhandler)   Registers a method that handles change events.Note  Before implementing an event handler, you should be familiar with the threading issues described in Understanding Threading Issues. |
| [IUIAutomation4::RemoveChangesEventHandler](nf-uiautomationclient-iuiautomation4-removechangeseventhandler)   Removes a changes event handler. |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 10, version 1607 [desktop apps only] |
| **Minimum supported server** | Windows Server 2016 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[IUIAutomation3](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomation3)

[UI Automation Element Interfaces for Clients](/en-us/windows/desktop/WinAuto/uiauto-entry-uiautoclientinterfaces)

---
