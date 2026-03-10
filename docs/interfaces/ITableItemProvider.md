# ITableItemProvider

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nn-uiautomationcore-itableitemprovider)

# ITableItemProvider interface (uiautomationcore.h)

Provides access
to child controls of containers that implement [ITableProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-itableprovider).

## Inheritance

The **ITableItemProvider** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **ITableItemProvider** also has these types of members:

## Methods

The **ITableItemProvider** interface has these methods.

|  |
| --- |
| [ITableItemProvider::GetColumnHeaderItems](nf-uiautomationcore-itableitemprovider-getcolumnheaderitems)   Retrieves a collection of Microsoft UI Automation provider representing all the column headers associated with a table item or cell. |
| [ITableItemProvider::GetRowHeaderItems](nf-uiautomationcore-itableitemprovider-getrowheaderitems)   Retrieves a collection of Microsoft UI Automation provider representing all the row headers associated with a table item or cell. |

## Remarks

This control pattern is analogous to [IGridItemProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-igriditemprovider) with
the distinction that any control implementing **ITableItemProvider**
must expose the relationship between the individual cell and its row and column information.

Access to individual cell functionality is provided by the concurrent implementation
of [IGridItemProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-igriditemprovider).

Implemented on a UI Automation provider that must
support the [TableItem](/en-us/windows/desktop/WinAuto/uiauto-implementingtableitem) control pattern.

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
