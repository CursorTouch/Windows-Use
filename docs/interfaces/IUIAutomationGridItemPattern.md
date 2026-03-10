# IUIAutomationGridItemPattern

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nn-uiautomationclient-iuiautomationgriditempattern)

# IUIAutomationGridItemPattern interface (uiautomationclient.h)

Provides access to a child control in a grid-style container that supports the [IUIAutomationGridPattern](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationgridpattern) interface.

## Inheritance

The **IUIAutomationGridItemPattern** interface inherits from the IUnknown interface.

## Methods

The **IUIAutomationGridItemPattern** interface has these methods.

|  |
| --- |
| [IUIAutomationGridItemPattern::get\_CachedColumn](nf-uiautomationclient-iuiautomationgriditempattern-get_cachedcolumn)   Retrieves the cached zero-based index of the column that contains the grid item. |
| [IUIAutomationGridItemPattern::get\_CachedColumnSpan](nf-uiautomationclient-iuiautomationgriditempattern-get_cachedcolumnspan)   Retrieves the cached number of columns spanned by the grid item. |
| [IUIAutomationGridItemPattern::get\_CachedContainingGrid](nf-uiautomationclient-iuiautomationgriditempattern-get_cachedcontaininggrid)   Retrieves the cached element that contains the grid item. |
| [IUIAutomationGridItemPattern::get\_CachedRow](nf-uiautomationclient-iuiautomationgriditempattern-get_cachedrow)   Retrieves the cached zero-based index of the row that contains the item. |
| [IUIAutomationGridItemPattern::get\_CachedRowSpan](nf-uiautomationclient-iuiautomationgriditempattern-get_cachedrowspan)   Retrieves the cached number of rows spanned by a grid item. |
| [IUIAutomationGridItemPattern::get\_CurrentColumn](nf-uiautomationclient-iuiautomationgriditempattern-get_currentcolumn)   Retrieves the zero-based index of the column that contains the item. |
| [IUIAutomationGridItemPattern::get\_CurrentColumnSpan](nf-uiautomationclient-iuiautomationgriditempattern-get_currentcolumnspan)   Retrieves the number of columns spanned by the grid item. |
| [IUIAutomationGridItemPattern::get\_CurrentContainingGrid](nf-uiautomationclient-iuiautomationgriditempattern-get_currentcontaininggrid)   Retrieves the element that contains the grid item. |
| [IUIAutomationGridItemPattern::get\_CurrentRow](nf-uiautomationclient-iuiautomationgriditempattern-get_currentrow)   Retrieves the zero-based index of the row that contains the grid item. |
| [IUIAutomationGridItemPattern::get\_CurrentRowSpan](nf-uiautomationclient-iuiautomationgriditempattern-get_currentrowspan)   Retrieves the number of rows spanned by the grid item. |

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
