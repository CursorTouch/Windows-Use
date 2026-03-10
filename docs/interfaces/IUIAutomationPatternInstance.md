# IUIAutomationPatternInstance

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nn-uiautomationcore-iuiautomationpatterninstance)

# IUIAutomationPatternInstance interface (uiautomationcore.h)

Represents a control pattern object. The client API wrapper uses this interface to implement all property and method calls in terms of the [GetProperty](/en-us/windows/desktop/api/uiautomationcore/nf-uiautomationcore-iuiautomationpatterninstance-getproperty) and [CallMethod](/en-us/windows/desktop/api/uiautomationcore/nf-uiautomationcore-iuiautomationpatterninstance-callmethod) methods.

## Inheritance

The **IUIAutomationPatternInstance** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **IUIAutomationPatternInstance** also has these types of members:

## Methods

The **IUIAutomationPatternInstance** interface has these methods.

|  |
| --- |
| [IUIAutomationPatternInstance::CallMethod](nf-uiautomationcore-iuiautomationpatterninstance-callmethod)   Client wrapper implements methods by calling this CallMethod function, specifying the parameters as an array of pointers. |
| [IUIAutomationPatternInstance::GetProperty](nf-uiautomationcore-iuiautomationpatterninstance-getproperty)   The client wrapper object implements the IUIAutomation::get\_CurrentX and IUIAutomationElement::get\_CachedX methods by calling this function, specifying the property by index. |

## Remarks

This interface is implemented by Microsoft UI Automation and returned by methods such as [GetCurrentPattern](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-getcurrentpattern). The interface is passed to [CreateClientWrapper](/en-us/windows/desktop/api/uiautomationcore/nf-uiautomationcore-iuiautomationpatternhandler-createclientwrapper), where it is used to call the appropriate methods and property getters.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[Control Pattern Interfaces for Clients](/en-us/windows/desktop/WinAuto/uiauto-client-controlpatterninterfaces)

---
