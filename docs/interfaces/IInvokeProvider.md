# IInvokeProvider

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nn-uiautomationcore-iinvokeprovider)

# IInvokeProvider interface (uiautomationcore.h)

Provides access to controls
that initiate or perform a single, unambiguous action and do not maintain state when activated.

## Inheritance

The **IInvokeProvider** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **IInvokeProvider** also has these types of members:

## Methods

The **IInvokeProvider** interface has these methods.

|  |
| --- |
| [IInvokeProvider::Invoke](nf-uiautomationcore-iinvokeprovider-invoke)   Sends a request to activate a control and initiate its single, unambiguous action. (IInvokeProvider.Invoke) |

## Remarks

Implemented on a Microsoft UI Automation provider that must
support the [Invoke](/en-us/windows/desktop/WinAuto/uiauto-implementinginvoke) control pattern.

Controls implement **IInvokeProvider** if the same behavior is not
exposed through another control pattern provider. For example, if
the [Invoke](/en-us/windows/desktop/api/uiautomationcore/nf-uiautomationcore-iinvokeprovider-invoke) method of a control performs the same
action as the [IExpandCollapseProvider::Expand](/en-us/windows/desktop/api/uiautomationcore/nf-uiautomationcore-iexpandcollapseprovider-expand) or [Collapse](/en-us/windows/desktop/api/uiautomationcore/nf-uiautomationcore-iexpandcollapseprovider-collapse)
method, the control should not also implement **IInvokeProvider**.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2003 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[UI Automation Providers Overview](/en-us/windows/desktop/WinAuto/uiauto-providersoverview)

---
