# IUIAutomationTablePattern

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nn-uiautomationclient-iuiautomationtablepattern)

# IUIAutomationTablePattern interface (uiautomationclient.h)

Provides access to a control that acts as a container for a collection of child elements. The children of this element support [IUIAutomationTableItemPattern](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationtableitempattern) and are organized in a two-dimensional logical coordinate system that can be traversed by row and column.

## Inheritance

The **IUIAutomationTablePattern** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **IUIAutomationTablePattern** also has these types of members:

## Methods

The **IUIAutomationTablePattern** interface has these methods.

|  |
| --- |
| [IUIAutomationTablePattern::get\_CachedRowOrColumnMajor](nf-uiautomationclient-iuiautomationtablepattern-get_cachedroworcolumnmajor)   Retrieves the cached primary direction of traversal for the table. |
| [IUIAutomationTablePattern::get\_CurrentRowOrColumnMajor](nf-uiautomationclient-iuiautomationtablepattern-get_currentroworcolumnmajor)   Retrieves the primary direction of traversal for the table. |
| [IUIAutomationTablePattern::GetCachedColumnHeaders](nf-uiautomationclient-iuiautomationtablepattern-getcachedcolumnheaders)   Retrieves a cached collection of UI Automation elements representing all the column headers in a table. |
| [IUIAutomationTablePattern::GetCachedRowHeaders](nf-uiautomationclient-iuiautomationtablepattern-getcachedrowheaders)   Retrieves a cached collection of UI Automation elements representing all the row headers in a table. |
| [IUIAutomationTablePattern::GetCurrentColumnHeaders](nf-uiautomationclient-iuiautomationtablepattern-getcurrentcolumnheaders)   Retrieves a collection of UI Automation elements representing all the column headers in a table. |
| [IUIAutomationTablePattern::GetCurrentRowHeaders](nf-uiautomationclient-iuiautomationtablepattern-getcurrentrowheaders)   Retrieves a collection of UI Automation elements representing all the row headers in a table. |

## Remarks

This control pattern is analogous to [IUIAutomationGridPattern](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationgridpattern) with the distinction that any control that supports **IUIAutomationTablePattern** also exposes a column or row header relationship, or both, for each child element. Controls that support the [Table](/en-us/windows/desktop/WinAuto/uiauto-implementingtableitem) control pattern also support the [Grid](/en-us/windows/desktop/WinAuto/uiauto-implementinggrid) control pattern in order to provide access to the inherent grid functionality of a table.

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
