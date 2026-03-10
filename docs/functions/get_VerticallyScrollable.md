# get_VerticallyScrollable

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nf-uiautomationcore-iscrollprovider-get_verticallyscrollable)

# IScrollProvider::get\_VerticallyScrollable method (uiautomationcore.h)

Indicates whether the control can scroll vertically.

This property is read-only.

## Syntax

```
HRESULT get_VerticallyScrollable(
  BOOL *pRetVal
);
```

## Parameters

`pRetVal`

## Return value

None

## Remarks

This property can be dynamic. For example, the content area of the control
might not be larger than the viewable area, meaning **IScrollProvider::VerticallyScrollable**
is **FALSE**. However, resizing the control or adding child items may increase the bounds of the
content area beyond the viewable area, meaning that **IScrollProvider::VerticallyScrollable** is **TRUE**.

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
