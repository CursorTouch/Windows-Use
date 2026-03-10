# IRawElementProviderFragmentRoot

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nn-uiautomationcore-irawelementproviderfragmentroot)

# IRawElementProviderFragmentRoot interface (uiautomationcore.h)

Exposes methods and properties on the root element in a fragment.

## Inheritance

The **IRawElementProviderFragmentRoot** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **IRawElementProviderFragmentRoot** also has these types of members:

## Methods

The **IRawElementProviderFragmentRoot** interface has these methods.

|  |
| --- |
| [IRawElementProviderFragmentRoot::ElementProviderFromPoint](nf-uiautomationcore-irawelementproviderfragmentroot-elementproviderfrompoint)   Retrieves the provider of the element that is at the specified point in this fragment. |
| [IRawElementProviderFragmentRoot::GetFocus](nf-uiautomationcore-irawelementproviderfragmentroot-getfocus)   Retrieves the element in this fragment that has the input focus. |

## Remarks

This interface is implemented by a root element within a framework; for example, a list box within a window.
Other elements in the same fragment, such as list items, implement the [IRawElementProviderFragment](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-irawelementproviderfragment) interface.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2003 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[IRawElementProviderFragment](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-irawelementproviderfragment)

[IRawElementProviderSimple](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-irawelementprovidersimple)

**Reference**

---
