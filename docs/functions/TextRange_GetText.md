# TextRange_GetText

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/nf-uiautomationcoreapi-textrange_gettext)

# TextRange\_GetText function (uiautomationcoreapi.h)

**Note**  This function is deprecated. Client applications should use the Microsoft UI Automation Component Object Model (COM) interfaces instead.

Returns the text in a text range, up to a specified number of characters.

## Syntax

```
HRESULT TextRange_GetText(
  [in]  HUIATEXTRANGE hobj,
  [in]  int           maxLength,
  [out] BSTR          *pRetVal
);
```

## Parameters

`[in] hobj`

Type: **HUIATEXTRANGE**

A text range object.

`[in] maxLength`

Type: **int**

The number of characters to return, beginning with the character at the starting endpoint of the text range.

`[out] pRetVal`

Type: **BSTR\***

When this function returns, this parameter contains
a pointer to the returned text.
This parameter is passed uninitialized.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

Returns S\_OK if successful or an error value otherwise.

## Remarks

If *maxLength* is -1, all of the text within the text range is returned.
If *maxLength* is larger than the length of the text range, the returned string contains all of the text in the text range.

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
