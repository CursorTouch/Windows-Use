# IUIAutomationSelectionItemPattern

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nn-uiautomationclient-iuiautomationselectionitempattern)

# IUIAutomationSelectionItemPattern interface (uiautomationclient.h)

Provides access to the selectable child items of a container control that supports [IUIAutomationSelectionPattern](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationselectionpattern).

## Inheritance

The **IUIAutomationSelectionItemPattern** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **IUIAutomationSelectionItemPattern** also has these types of members:

## Methods

The **IUIAutomationSelectionItemPattern** interface has these methods.

|  |
| --- |
| [IUIAutomationSelectionItemPattern::AddToSelection](nf-uiautomationclient-iuiautomationselectionitempattern-addtoselection)   Adds the current element to the collection of selected items. (IUIAutomationSelectionItemPattern.AddToSelection) |
| [IUIAutomationSelectionItemPattern::get\_CachedIsSelected](nf-uiautomationclient-iuiautomationselectionitempattern-get_cachedisselected)   A cached value that indicates whether this item is selected. |
| [IUIAutomationSelectionItemPattern::get\_CachedSelectionContainer](nf-uiautomationclient-iuiautomationselectionitempattern-get_cachedselectioncontainer)   Retrieves the cached element that supports IUIAutomationSelectionPattern and acts as the container for this item. |
| [IUIAutomationSelectionItemPattern::get\_CurrentIsSelected](nf-uiautomationclient-iuiautomationselectionitempattern-get_currentisselected)   Indicates whether this item is selected. |
| [IUIAutomationSelectionItemPattern::get\_CurrentSelectionContainer](nf-uiautomationclient-iuiautomationselectionitempattern-get_currentselectioncontainer)   Retrieves the element that supports IUIAutomationSelectionPattern and acts as the container for this item. |
| [IUIAutomationSelectionItemPattern::RemoveFromSelection](nf-uiautomationclient-iuiautomationselectionitempattern-removefromselection)   Removes this element from the selection. |
| [IUIAutomationSelectionItemPattern::Select](nf-uiautomationclient-iuiautomationselectionitempattern-select)   Clears any selected items and then selects the current element. |

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
