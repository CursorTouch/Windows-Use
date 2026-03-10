# ISpreadsheetItemProvider

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nn-uiautomationcore-ispreadsheetitemprovider)

# ISpreadsheetItemProvider interface (uiautomationcore.h)

Provides access
to information about an item (cell) in a spreadsheet.

## Inheritance

The **ISpreadsheetItemProvider** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **ISpreadsheetItemProvider** also has these types of members:

## Methods

The **ISpreadsheetItemProvider** interface has these methods.

|  |
| --- |
| [ISpreadsheetItemProvider::get\_Formula](nf-uiautomationcore-ispreadsheetitemprovider-get_formula)   Specifies the formula for this spreadsheet cell. |
| [ISpreadsheetItemProvider::GetAnnotationObjects](nf-uiautomationcore-ispreadsheetitemprovider-getannotationobjects)   Retrieves an array of objects that represent the annotations associated with this spreadsheet cell. |
| [ISpreadsheetItemProvider::GetAnnotationTypes](nf-uiautomationcore-ispreadsheetitemprovider-getannotationtypes)   Retrieves an array of annotation type identifiers indicating the types of annotations that are associated with this spreadsheet cell. (ISpreadsheetItemProvider.GetAnnotationTypes) |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 8 [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2012 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[Control Pattern Interfaces for Providers](/en-us/windows/desktop/WinAuto/uiauto-cpinterfaces)

---
