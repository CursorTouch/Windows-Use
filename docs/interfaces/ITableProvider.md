# ITableProvider

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nn-uiautomationcore-itableprovider)

# ITableProvider interface (uiautomationcore.h)

Provides access to controls that act as containers for a collection of child elements. The children of this element must implement [ITableItemProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-itableitemprovider) and be organized in a two-dimensional logical coordinate system that can be traversed by using the keyboard.

## Inheritance

The **ITableProvider** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **ITableProvider** also has these types of members:

## Methods

The **ITableProvider** interface has these methods.

|  |
| --- |
| [ITableProvider::get\_RowOrColumnMajor](nf-uiautomationcore-itableprovider-get_roworcolumnmajor)   Specifies the primary direction of traversal for the table. |
| [ITableProvider::GetColumnHeaders](nf-uiautomationcore-itableprovider-getcolumnheaders)   Gets a collection of Microsoft UI Automation providers that represents all the column headers in a table. |
| [ITableProvider::GetRowHeaders](nf-uiautomationcore-itableprovider-getrowheaders)   Gets a collection of Microsoft UI Automation providers that represents all the row headers in a table. |

## Remarks

This control pattern is analogous to [IGridProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-igridprovider) with the distinction that any control that implements **ITableProvider** must also expose a column and/or row header relationship for each child element.

Controls that implement **ITableProvider** are also required to implement [IGridProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-igridprovider) so as to expose the inherent grid functionality of a table control.

Implemented on a UI Automation provider that must support the [Table](/en-us/windows/desktop/WinAuto/uiauto-implementingtable) control pattern and [Grid](/en-us/windows/desktop/WinAuto/uiauto-implementinggrid) control pattern.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2003 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[UI Automation Providers Overview](/en-us/windows/desktop/WinAuto/uiauto-providersoverview)

---
