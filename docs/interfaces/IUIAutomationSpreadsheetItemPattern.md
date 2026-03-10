# IUIAutomationSpreadsheetItemPattern

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nn-uiautomationclient-iuiautomationspreadsheetitempattern)

# IUIAutomationSpreadsheetItemPattern interface (uiautomationclient.h)

Enables a client application to retrieve information about an item (cell) in a spreadsheet.

## Inheritance

The **IUIAutomationSpreadsheetItemPattern** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **IUIAutomationSpreadsheetItemPattern** also has these types of members:

## Methods

The **IUIAutomationSpreadsheetItemPattern** interface has these methods.

|  |
| --- |
| [IUIAutomationSpreadsheetItemPattern::get\_CachedFormula](nf-uiautomationclient-iuiautomationspreadsheetitempattern-get_cachedformula)   Retrieves the cached formula for this cell. |
| [IUIAutomationSpreadsheetItemPattern::get\_CurrentFormula](nf-uiautomationclient-iuiautomationspreadsheetitempattern-get_currentformula)   Retrieves the formula for this cell. |
| [IUIAutomationSpreadsheetItemPattern::GetCachedAnnotationObjects](nf-uiautomationclient-iuiautomationspreadsheetitempattern-getcachedannotationobjects)   Retrieves a cached array of elements representing the annotations associated with this spreadsheet cell. |
| [IUIAutomationSpreadsheetItemPattern::GetCachedAnnotationTypes](nf-uiautomationclient-iuiautomationspreadsheetitempattern-getcachedannotationtypes)   Retrieves a cached array of annotation type identifiers indicating the types of annotations that are associated with this spreadsheet cell. |
| [IUIAutomationSpreadsheetItemPattern::GetCurrentAnnotationObjects](nf-uiautomationclient-iuiautomationspreadsheetitempattern-getcurrentannotationobjects)   Retrieves an array of elements representing the annotations associated with this spreadsheet cell. |
| [IUIAutomationSpreadsheetItemPattern::GetCurrentAnnotationTypes](nf-uiautomationclient-iuiautomationspreadsheetitempattern-getcurrentannotationtypes)   Retrieves an array of annotation type identifiers indicating the types of annotations that are associated with this spreadsheet cell. (IUIAutomationSpreadsheetItemPattern.GetCurrentAnnotationTypes) |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 8 [desktop apps only] |
| **Minimum supported server** | Windows Server 2012 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[Control Pattern Interfaces for Clients](/en-us/windows/desktop/WinAuto/uiauto-client-controlpatterninterfaces)

---
