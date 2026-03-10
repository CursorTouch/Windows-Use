# SetScrollPercent

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nf-uiautomationcore-iscrollprovider-setscrollpercent)

# IScrollProvider::SetScrollPercent method (uiautomationcore.h)

Sets the horizontal and vertical scroll position as a percentage of the total content area within the control.

## Syntax

```
HRESULT SetScrollPercent(
  [in] double horizontalPercent,
  [in] double verticalPercent
);
```

## Parameters

`[in] horizontalPercent`

Type: **double**

The horizontal position as a percentage of the content area's total range, or **UIA\_ScrollPatternNoScroll** if there is no horizontal scrolling.

`[in] verticalPercent`

Type: **double**

The vertical position as a percentage of the content area's total range, or **UIA\_ScrollPatternNoScroll** if there is no vertical scrolling.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

This method is only useful when the content area of the control is
larger than the visible region.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2003 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[IScrollProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-iscrollprovider)

[UI Automation Providers Overview](/en-us/windows/desktop/WinAuto/uiauto-providersoverview)

---
