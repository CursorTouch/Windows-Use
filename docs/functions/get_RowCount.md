# get_RowCount

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nf-uiautomationcore-igridprovider-get_rowcount)

# IGridProvider::get\_RowCount method (uiautomationcore.h)

Specifies the total number of rows in the grid.

This property is read-only.

## Syntax

```
HRESULT get_RowCount(
  int *pRetVal
);
```

## Parameters

`pRetVal`

## Return value

None

## Remarks

Hidden rows and columns, depending on the provider implementation, may be loaded
in the logical tree and will therefore be reflected in the
**IGridProvider::RowCount** and
[IGridProvider::ColumnCount](/en-us/windows/desktop/api/uiautomationcore/nf-uiautomationcore-igridprovider-get_columncount) properties.
If the hidden rows and columns have not yet been loaded they will not be counted.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2003 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |
| **DLL** | Uiautomationcore.dll |

## See also

[IGridProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-igridprovider)

[UI Automation Providers Overview](/en-us/windows/desktop/WinAuto/uiauto-providersoverview)

---
