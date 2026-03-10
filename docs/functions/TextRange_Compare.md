# TextRange_Compare

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/nf-uiautomationcoreapi-textrange_compare)

# TextRange\_Compare function (uiautomationcoreapi.h)

**Note**  This function is deprecated. Client applications should use the Microsoft UI Automation Component Object Model (COM) interfaces instead.

Compares two text ranges.

## Syntax

```
HRESULT TextRange_Compare(
  [in]  HUIATEXTRANGE hobj,
  [in]  HUIATEXTRANGE range,
  [out] BOOL          *pRetVal
);
```

## Parameters

`[in] hobj`

Type: **HUIATEXTRANGE**

The first text range to compare.

`[in] range`

Type: **HUIATEXTRANGE**

The second text range to compare.

`[out] pRetVal`

Type: **[BOOL](/en-us/windows/desktop/WinProg/windows-data-types)\***

When this function returns, contains **TRUE** if the two objects span the same text; otherwise **FALSE**.
This parameter is passed uninitialized.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

Returns S\_OK if successful or an error value otherwise.

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
