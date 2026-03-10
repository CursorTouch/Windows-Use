# IUIAutomationExpandCollapsePattern

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nn-uiautomationclient-iuiautomationexpandcollapsepattern)

# IUIAutomationExpandCollapsePattern interface (uiautomationclient.h)

Provides access to a control that can visually expand to display content, and collapse to hide content.

## Inheritance

The **IUIAutomationExpandCollapsePattern** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **IUIAutomationExpandCollapsePattern** also has these types of members:

## Methods

The **IUIAutomationExpandCollapsePattern** interface has these methods.

|  |
| --- |
| [IUIAutomationExpandCollapsePattern::Collapse](nf-uiautomationclient-iuiautomationexpandcollapsepattern-collapse)   Hides all child nodes, controls, or content of the element. |
| [IUIAutomationExpandCollapsePattern::Expand](nf-uiautomationclient-iuiautomationexpandcollapsepattern-expand)   Displays all child nodes, controls, or content of the element. |
| [IUIAutomationExpandCollapsePattern::get\_CachedExpandCollapseState](nf-uiautomationclient-iuiautomationexpandcollapsepattern-get_cachedexpandcollapsestate)   Retrieves a cached value that indicates the state, expanded or collapsed, of the element. |
| [IUIAutomationExpandCollapsePattern::get\_CurrentExpandCollapseState](nf-uiautomationclient-iuiautomationexpandcollapsepattern-get_currentexpandcollapsestate)   Retrieves a value that indicates the state, expanded or collapsed, of the element. |

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
