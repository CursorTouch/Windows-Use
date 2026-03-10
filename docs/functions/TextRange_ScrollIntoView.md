# TextRange_ScrollIntoView

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/nf-uiautomationcoreapi-textrange_scrollintoview)

# TextRange\_ScrollIntoView function (uiautomationcoreapi.h)

**Note**  This function is deprecated. Client applications should use the Microsoft UI Automation Component Object Model (COM) interfaces instead.

Scrolls the text so the specified range is visible in the viewport.

## Syntax

```
HRESULT TextRange_ScrollIntoView(
  [in] HUIATEXTRANGE hobj,
  [in] BOOL          alignToTop
);
```

## Parameters

`[in] hobj`

Type: **HUIATEXTRANGE**

The text range to scroll.

`[in] alignToTop`

Type: **[BOOL](/en-us/windows/desktop/WinProg/windows-data-types)**

TRUE to align the top of the text range with the top of the viewport;
FALSE to align the bottom of the text range with the bottom of the viewport.

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
