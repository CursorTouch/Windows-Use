# IGridItemProvider

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nn-uiautomationcore-igriditemprovider)

# IGridItemProvider interface (uiautomationcore.h)

Provides access
to individual child controls of containers that implement [IGridProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-igridprovider).

## Inheritance

The **IGridItemProvider** interface inherits from the IUnknown interface.

## Methods

The **IGridItemProvider** interface has these methods.

|  |
| --- |
| [IGridItemProvider::get\_Column](nf-uiautomationcore-igriditemprovider-get_column)   Specifies the ordinal number of the column that contains this cell or item. |
| [IGridItemProvider::get\_ColumnSpan](nf-uiautomationcore-igriditemprovider-get_columnspan)   Specifies the number of columns spanned by this cell or item. |
| [IGridItemProvider::get\_ContainingGrid](nf-uiautomationcore-igriditemprovider-get_containinggrid)   Specifies the UI Automation provider that implements IGridProvider and represents the container of this cell or item. |
| [IGridItemProvider::get\_Row](nf-uiautomationcore-igriditemprovider-get_row)   Specifies the ordinal number of the row that contains this cell or item. |
| [IGridItemProvider::get\_RowSpan](nf-uiautomationcore-igriditemprovider-get_rowspan)   Specifies the number of rows spanned by this cell or item. |

## Remarks

Implemented on a UI Automation provider that must support the [GridItem](/en-us/windows/desktop/WinAuto/uiauto-implementinggriditem) *control pattern*.

Controls that implement **IGridItemProvider** can typically be traversed
(that is, a UI Automation client can move to adjacent controls) by using the keyboard.

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
