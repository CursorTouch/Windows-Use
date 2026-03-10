# IUIAutomation3

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nn-uiautomationclient-iuiautomation3)

# IUIAutomation3 interface (uiautomationclient.h)

Extends the [IUIAutomation2](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomation2) interface to expose additional methods for controlling Microsoft UI Automation functionality.

## Inheritance

The **IUIAutomation3** interface inherits from [IUIAutomation2](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomation2). **IUIAutomation3** also has these types of members:

## Methods

The **IUIAutomation3** interface has these methods.

|  |
| --- |
| [IUIAutomation3::AddTextEditTextChangedEventHandler](nf-uiautomationclient-iuiautomation3-addtextedittextchangedeventhandler)   Registers a method that handles programmatic text-edit events.Note  Before implementing an event handler, you should be familiar with the threading issues described in Understanding Threading Issues. |
| [IUIAutomation3::RemoveTextEditTextChangedEventHandler](nf-uiautomationclient-iuiautomation3-removetextedittextchangedeventhandler)   Removes a programmatic text-edit event handler. |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 8.1 [desktop apps only] |
| **Minimum supported server** | Windows Server 2012 R2 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[IUIAutomation2](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomation2)

[UI Automation Element Interfaces for Clients](/en-us/windows/desktop/WinAuto/uiauto-entry-uiautoclientinterfaces)

---
