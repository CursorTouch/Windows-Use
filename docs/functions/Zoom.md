# Zoom

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nf-uiautomationcore-itransformprovider2-zoom)

# ITransformProvider2::Zoom method (uiautomationcore.h)

Zooms the viewport of the control.

## Syntax

```
HRESULT Zoom(
  [in] double zoom
);
```

## Parameters

`[in] zoom`

Type: **double**

The amount to zoom the viewport, specified as a percentage. The provider should zoom the viewport to the nearest supported value.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

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
