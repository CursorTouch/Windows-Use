# IUIAutomationSelectionPattern

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nn-uiautomationclient-iuiautomationselectionpattern)

# IUIAutomationSelectionPattern interface (uiautomationclient.h)

Provides access to a control that contains selectable child items. The children of this element support [IUIAutomationSelectionItemPattern](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationselectionitempattern).

## Inheritance

The **IUIAutomationSelectionPattern** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **IUIAutomationSelectionPattern** also has these types of members:

## Methods

The **IUIAutomationSelectionPattern** interface has these methods.

|  |
| --- |
| [IUIAutomationSelectionPattern::get\_CachedCanSelectMultiple](nf-uiautomationclient-iuiautomationselectionpattern-get_cachedcanselectmultiple)   Retrieves a cached value that indicates whether more than one item in the container can be selected at one time. |
| [IUIAutomationSelectionPattern::get\_CachedIsSelectionRequired](nf-uiautomationclient-iuiautomationselectionpattern-get_cachedisselectionrequired)   Retrieves a cached value that indicates whether at least one item must be selected at all times. |
| [IUIAutomationSelectionPattern::get\_CurrentCanSelectMultiple](nf-uiautomationclient-iuiautomationselectionpattern-get_currentcanselectmultiple)   Indicates whether more than one item in the container can be selected at one time. |
| [IUIAutomationSelectionPattern::get\_CurrentIsSelectionRequired](nf-uiautomationclient-iuiautomationselectionpattern-get_currentisselectionrequired)   Indicates whether at least one item must be selected at all times. |
| [IUIAutomationSelectionPattern::GetCachedSelection](nf-uiautomationclient-iuiautomationselectionpattern-getcachedselection)   Retrieves the cached selected elements in the container. |
| [IUIAutomationSelectionPattern::GetCurrentSelection](nf-uiautomationclient-iuiautomationselectionpattern-getcurrentselection)   Retrieves the selected elements in the container. |

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
