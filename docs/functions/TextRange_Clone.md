# TextRange_Clone

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/nf-uiautomationcoreapi-textrange_clone)

# TextRange\_Clone function (uiautomationcoreapi.h)

**Note**  This function is deprecated. Client applications should use the Microsoft UI Automation Component Object Model (COM) interfaces instead.

Copies a text range.

## Syntax

```
HRESULT TextRange_Clone(
  [in]  HUIATEXTRANGE hobj,
  [out] HUIATEXTRANGE *pRetVal
);
```

## Parameters

`[in] hobj`

Type: **HUIATEXTRANGE**

A text range object.

`[out] pRetVal`

Type: **HUIATEXTRANGE\***

When this function returns, contains the copy.
This parameter is passed uninitialized.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

Returns S\_OK if successful or an error value otherwise.

## Remarks

The method never returns **NULL** (Nothing in Microsoft Visual Basic .NET).

The new range can be manipulated independently from the original.

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
