# ScrollPattern_Scroll

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/nf-uiautomationcoreapi-scrollpattern_scroll)

# ScrollPattern\_Scroll function (uiautomationcoreapi.h)

**Note**  This function is deprecated. Client applications should use the Microsoft UI Automation Component Object Model (COM) interfaces instead.

Scrolls the currently visible region of the content area the specified [ScrollAmount](/en-us/windows/desktop/api/uiautomationcore/ne-uiautomationcore-scrollamount), horizontally,
vertically, or both.

## Syntax

```
HRESULT ScrollPattern_Scroll(
  [in] HUIAPATTERNOBJECT hobj,
  [in] ScrollAmount      horizontalAmount,
  [in] ScrollAmount      verticalAmount
);
```

## Parameters

`[in] hobj`

Type: **HUIAPATTERNOBJECT**

The control pattern object.

`[in] horizontalAmount`

Type: **[ScrollAmount](/en-us/windows/desktop/api/uiautomationcore/ne-uiautomationcore-scrollamount)**

The amount to scroll the container on the horizontal axis, as a percentage.

`[in] verticalAmount`

Type: **[ScrollAmount](/en-us/windows/desktop/api/uiautomationcore/ne-uiautomationcore-scrollamount)**

The amount to scroll the container on the vertical axis, as a percentage.

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
