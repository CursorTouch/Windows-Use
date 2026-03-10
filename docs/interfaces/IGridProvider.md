# IGridProvider

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nn-uiautomationcore-igridprovider)

# IGridProvider interface (uiautomationcore.h)

Provides access to
controls that act as containers for a collection of child elements organized in a two-dimensional
logical coordinate system that can be traversed (that is, a Microsoft UI Automation client can
move to adjacent controls) by using the keyboard. The children of this
element must implement [IGridItemProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-igriditemprovider).

## Inheritance

The **IGridProvider** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **IGridProvider** also has these types of members:

## Methods

The **IGridProvider** interface has these methods.

|  |
| --- |
| [IGridProvider::get\_ColumnCount](nf-uiautomationcore-igridprovider-get_columncount)   Specifies the total number of columns in the grid. |
| [IGridProvider::get\_RowCount](nf-uiautomationcore-igridprovider-get_rowcount)   Specifies the total number of rows in the grid. |
| [IGridProvider::GetItem](nf-uiautomationcore-igridprovider-getitem)   Retrieves the Microsoft UI Automation provider for the specified cell. |

## Remarks

The **IGridProvider** interface exposes methods and properties to support UI Automation client access to controls
that act as containers for a collection of child elements. The children of this element must implement [IGridItemProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-igriditemprovider) and be organized in a two-dimensional logical coordinate system that can be traversed (that is, a UI Automation client can move to adjacent controls) by using the keyboard.

Implemented on a UI Automation provider that must support
the [Grid](/en-us/windows/desktop/WinAuto/uiauto-implementinggrid) control pattern.

**IGridProvider** does not enable active manipulation of a grid;
[ITransformProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-itransformprovider) must be implemented for this.

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
