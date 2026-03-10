# IUIAutomationInvokePattern

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nn-uiautomationclient-iuiautomationinvokepattern)

# IUIAutomationInvokePattern interface (uiautomationclient.h)

Exposes a method that enables a client application to invoke the action of a control (typically a button).

## Inheritance

The **IUIAutomationInvokePattern** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **IUIAutomationInvokePattern** also has these types of members:

## Methods

The **IUIAutomationInvokePattern** interface has these methods.

|  |
| --- |
| [IUIAutomationInvokePattern::Invoke](nf-uiautomationclient-iuiautomationinvokepattern-invoke)   Invokes the action of a control, such as a button click. |

## Remarks

A control should support this interface if it initiates or performs a single, unambiguous action and does not maintain state when activated.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[Control Pattern Interfaces for Clients](/en-us/windows/desktop/WinAuto/uiauto-client-controlpatterninterfaces)

---
