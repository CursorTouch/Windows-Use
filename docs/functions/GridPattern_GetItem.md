# GridPattern_GetItem

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/nf-uiautomationcoreapi-gridpattern_getitem)

# GridPattern\_GetItem function (uiautomationcoreapi.h)

**Note**  This function is deprecated. Client applications should use the Microsoft UI Automation Component Object Model (COM) interfaces instead.

Gets the node for an item in a grid.

## Syntax

```
HRESULT GridPattern_GetItem(
  [in]  HUIAPATTERNOBJECT hobj,
  [in]  int               row,
  [in]  int               column,
  [out] HUIANODE          *pResult
);
```

## Parameters

`[in] hobj`

Type: **HUIAPATTERNOBJECT**

The *control pattern* object.

`[in] row`

Type: **int**

The row of the node being requested.

`[in] column`

Type: **int**

The column of the node being requested.

`[out] pResult`

Type: **HUIANODE\***

When this function returns, contains a pointer to the node for the cell
at the specified location. This parameter is passed uninitialized.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

Returns S\_OK if successful or an error value otherwise.

## Remarks

Row 0, column 0 is the first item in a grid.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps only] |
| **Minimum supported server** | Windows Server 2003 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationcoreapi.h |
| **Library** | Uiautomationcore.lib |
| **DLL** | Uiautomationcore.dll |

---
