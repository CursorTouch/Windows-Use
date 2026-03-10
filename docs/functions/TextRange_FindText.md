# TextRange_FindText

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/nf-uiautomationcoreapi-textrange_findtext)

# TextRange\_FindText function (uiautomationcoreapi.h)

**Note**  This function is deprecated. Client applications should use the Microsoft UI Automation Component Object Model (COM) interfaces instead.

Returns the first text range in the specified direction that contains the text the client is searching for.

## Syntax

```
HRESULT TextRange_FindText(
  [in]  HUIATEXTRANGE hobj,
  [in]  BSTR          text,
  [in]  BOOL          backward,
  [in]  BOOL          ignoreCase,
  [out] HUIATEXTRANGE *pRetVal
);
```

## Parameters

`[in] hobj`

Type: **HUIATEXTRANGE**

The text range to search.

`[in] text`

Type: **BSTR**

The string to search for.

`[in] backward`

Type: **[BOOL](/en-us/windows/desktop/WinProg/windows-data-types)**

**TRUE** to search backward; otherwise **FALSE**.

`[in] ignoreCase`

Type: **[BOOL](/en-us/windows/desktop/WinProg/windows-data-types)**

**TRUE** to specify a case-insensitive search; otherwise **FALSE**.

`[out] pRetVal`

Type: **HUITEXTRANGE\***

When this function returns, contains
the text range for the first span of text that matches the string
the client is searching for.
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
