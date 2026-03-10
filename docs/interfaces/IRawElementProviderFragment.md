# IRawElementProviderFragment

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nn-uiautomationcore-irawelementproviderfragment)

# IRawElementProviderFragment interface (uiautomationcore.h)

Exposes methods and properties on UI elements that are part of a structure more than one level deep,
such as a list box or list item. Implemented by Microsoft UI Automation provider.

## Inheritance

The **IRawElementProviderFragment** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **IRawElementProviderFragment** also has these types of members:

## Methods

The **IRawElementProviderFragment** interface has these methods.

|  |
| --- |
| [IRawElementProviderFragment::get\_BoundingRectangle](nf-uiautomationcore-irawelementproviderfragment-get_boundingrectangle)   Specifies the bounding rectangle of this element. |
| [IRawElementProviderFragment::get\_FragmentRoot](nf-uiautomationcore-irawelementproviderfragment-get_fragmentroot)   Specifies the root node of the fragment. |
| [IRawElementProviderFragment::GetEmbeddedFragmentRoots](nf-uiautomationcore-irawelementproviderfragment-getembeddedfragmentroots)   Retrieves an array of root fragments that are embedded in the Microsoft UI Automation tree rooted at the current element. |
| [IRawElementProviderFragment::GetRuntimeId](nf-uiautomationcore-irawelementproviderfragment-getruntimeid)   Retrieves the runtime identifier of an element. |
| [IRawElementProviderFragment::Navigate](nf-uiautomationcore-irawelementproviderfragment-navigate)   Retrieves the Microsoft UI Automation element in a specified direction within the UI Automation tree. |
| [IRawElementProviderFragment::SetFocus](nf-uiautomationcore-irawelementproviderfragment-setfocus)   Sets the focus to this element. |

## Remarks

The root node of the fragment must also support the [IRawElementProviderFragmentRoot](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-irawelementproviderfragmentroot) interface.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2003 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[IRawElementProviderFragmentRoot](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-irawelementproviderfragmentroot)

[IRawElementProviderSimple](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-irawelementprovidersimple)

**Reference**

---
