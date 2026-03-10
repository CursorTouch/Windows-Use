# get_VerticalScrollPercent

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nf-uiautomationcore-iscrollprovider-get_verticalscrollpercent)

# IScrollProvider::get\_VerticalScrollPercent method (uiautomationcore.h)

Specifies the vertical scroll position.

This property is read-only.

## Syntax

```
HRESULT get_VerticalScrollPercent(
  double *pRetVal
);
```

## Parameters

`pRetVal`

## Return value

None

## Remarks

The vertical scroll position can be reported as **UIA\_ScrollPatternNoScroll** if no valid position is available; for example, if the window does not have a vertical scroll bar.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2003 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

**Conceptual**

[HorizontalScrollPercent](/en-us/windows/desktop/api/uiautomationcore/nf-uiautomationcore-iscrollprovider-get_horizontalscrollpercent)

[IScrollProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-iscrollprovider)

**Reference**

[UI Automation Providers Overview](/en-us/windows/desktop/WinAuto/uiauto-providersoverview)

---
