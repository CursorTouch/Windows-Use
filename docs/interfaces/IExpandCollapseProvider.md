# IExpandCollapseProvider

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nn-uiautomationcore-iexpandcollapseprovider)

# IExpandCollapseProvider interface (uiautomationcore.h)

Provides
access to a control that visually expands to display content, and collapses to hide content.

## Inheritance

The **IExpandCollapseProvider** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **IExpandCollapseProvider** also has these types of members:

## Methods

The **IExpandCollapseProvider** interface has these methods.

|  |
| --- |
| [IExpandCollapseProvider::Collapse](nf-uiautomationcore-iexpandcollapseprovider-collapse)   Hides all child nodes, controls, or content of this element. |
| [IExpandCollapseProvider::Expand](nf-uiautomationcore-iexpandcollapseprovider-expand)   Displays all child nodes, controls, or content of the control. |
| [IExpandCollapseProvider::get\_ExpandCollapseState](nf-uiautomationcore-iexpandcollapseprovider-get_expandcollapsestate)   Indicates the state, expanded or collapsed, of the control. |

## Remarks

Implemented on a Microsoft UI Automation provider that must support the [ExpandCollapse](/en-us/windows/desktop/WinAuto/uiauto-implementingexpandcollapse) control pattern.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2003 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

**Conceptual**

[ExpandCollapseState](/en-us/windows/desktop/api/uiautomationcore/ne-uiautomationcore-expandcollapsestate)

**Reference**

[UI Automation Providers Overview](/en-us/windows/desktop/WinAuto/uiauto-providersoverview)

---
