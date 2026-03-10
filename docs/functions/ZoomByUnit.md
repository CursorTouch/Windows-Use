# ZoomByUnit

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nf-uiautomationcore-itransformprovider2-zoombyunit)

# ITransformProvider2::ZoomByUnit method (uiautomationcore.h)

Zooms the viewport of the control by the specified logical unit.

## Syntax

```
HRESULT ZoomByUnit(
  ZoomUnit zoomUnit
);
```

## Parameters

`zoomUnit`

The logical unit by which to increase or decrease the zoom of the viewport.

## Return value

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 8 [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2012 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[ITransformProvider2](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-itransformprovider2)

---
