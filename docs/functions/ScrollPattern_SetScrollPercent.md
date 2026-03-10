# ScrollPattern_SetScrollPercent

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/nf-uiautomationcoreapi-scrollpattern_setscrollpercent)

# ScrollPattern\_SetScrollPercent function (uiautomationcoreapi.h)

**Note**  This function is deprecated. Client applications should use the Microsoft UI Automation Component Object Model (COM) interfaces instead.

Scrolls a container to a specific position horizontally, vertically, or both.

## Syntax

```
HRESULT ScrollPattern_SetScrollPercent(
  [in] HUIAPATTERNOBJECT hobj,
  [in] double            horizontalPercent,
  [in] double            verticalPercent
);
```

## Parameters

`[in] hobj`

Type: **HUIAPATTERNOBJECT**

The control pattern object.

`[in] horizontalPercent`

Type: **double**

The horizontal position to scroll to.

`[in] verticalPercent`

Type: **double**

The vertical position to scroll to.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

Returns S\_OK if successful or an error value otherwise.

## Remarks

The scroll area is normalized to range from 0.0 to 100.0. If the position is set to 0.0, the control
scrolls to the beginning of the
visible region, and if the position is set to 100.0, it scrolls to the end of the visible region.
Pass -1.0 for the percent parameters if no scrolling occurs on that axis.

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
