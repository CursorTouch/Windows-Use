# get_HorizontalScrollPercent

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nf-uiautomationcore-iscrollprovider-get_horizontalscrollpercent)

# IScrollProvider::get\_HorizontalScrollPercent method (uiautomationcore.h)

Specifies the horizontal scroll position.

This property is read-only.

## Syntax

```
HRESULT get_HorizontalScrollPercent(
  double *pRetVal
);
```

## Parameters

`pRetVal`

## Return value

None

## Remarks

The horizontal scroll position can be reported as **UIA\_ScrollPatternNoScroll** if no valid position is available; for example, if the window does not have a horizontal scroll bar.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2003 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

**Conceptual**

[IScrollProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-iscrollprovider)

**Reference**

[UI Automation Providers Overview](/en-us/windows/desktop/WinAuto/uiauto-providersoverview)

[VerticalScrollPercent](/en-us/windows/desktop/api/uiautomationcore/nf-uiautomationcore-iscrollprovider-get_verticalscrollpercent)

---
