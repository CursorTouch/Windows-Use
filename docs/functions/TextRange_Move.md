# TextRange_Move

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/nf-uiautomationcoreapi-textrange_move)

# TextRange\_Move function (uiautomationcoreapi.h)

**Note**  This function is deprecated. Client applications should use the Microsoft UI Automation Component Object Model (COM) interfaces instead.

Moves the text range the specified number of units requested by the client.

## Syntax

```
HRESULT TextRange_Move(
  [in]  HUIATEXTRANGE hobj,
  [in]  TextUnit      unit,
  [in]  int           count,
  [out] int           *pRetVal
);
```

## Parameters

`[in] hobj`

Type: **HUIATEXTRANGE**

A text range object.

`[in] unit`

Type: **[TextUnit](/en-us/windows/desktop/api/uiautomationcore/ne-uiautomationcore-textunit)**

The unit, such as Page, Line, or Word.

`[in] count`

Type: **int**

The number of units to move. Positive numbers move the range forward,
and negative numbers move the range backward.

`[out] pRetVal`

Type: **int\***

When this function returns, contains
the number of units actually moved.
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
