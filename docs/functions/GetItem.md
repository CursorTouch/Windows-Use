# GetItem

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nf-uiautomationcore-igridprovider-getitem)

# IGridProvider::GetItem method (uiautomationcore.h)

Retrieves the Microsoft UI Automation provider for the specified cell.

## Syntax

```
HRESULT GetItem(
  [in]          int                       row,
  [in]          int                       column,
  [out, retval] IRawElementProviderSimple **pRetVal
);
```

## Parameters

`[in] row`

Type: **int**

The ordinal number of the row of interest.

`[in] column`

Type: **int**

The ordinal number of the column of interest.

`[out, retval] pRetVal`

Type: **[IRawElementProviderSimple](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-irawelementprovidersimple)\*\***

Receives a pointer to a UI Automation provider for the specified cell or a null reference
(Nothing in Microsoft Visual Basic .NET) if the cell is empty.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

Grid coordinates are zero-based with the upper left (or upper right cell depending on locale) having coordinates (0,0).

If a cell is empty a UI Automation provider must still be
returned in order to support the [ContainingGrid](/en-us/windows/desktop/api/uiautomationcore/nf-uiautomationcore-igriditemprovider-get_containinggrid) property
for that cell. This is possible when the layout of child elements in the grid is similar to a ragged array.

Hidden rows and columns, depending on the provider implementation, may be loaded in the
UI Automation tree and will therefore be reflected in the [IGridProvider::RowCount](/en-us/windows/desktop/api/uiautomationcore/nf-uiautomationcore-igridprovider-get_rowcount)
and [IGridProvider::ColumnCount](/en-us/windows/desktop/api/uiautomationcore/nf-uiautomationcore-igridprovider-get_columncount) properties.
If the hidden rows and columns have not yet been loaded they should not be counted.

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
