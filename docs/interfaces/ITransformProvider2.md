# ITransformProvider2

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nn-uiautomationcore-itransformprovider2)

# ITransformProvider2 interface (uiautomationcore.h)

Extends the [ITransformProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-itransformprovider) interface to enable Microsoft UI Automation providers to expose properties to support the viewport zooming functionality of a control.

## Inheritance

The **ITransformProvider2** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **ITransformProvider2** also has these types of members:

## Methods

The **ITransformProvider2** interface has these methods.

|  |
| --- |
| [ITransformProvider2::get\_CanZoom](nf-uiautomationcore-itransformprovider2-get_canzoom)   Indicates whether the control supports zooming of its viewport. (ITransformProvider2.get\_CanZoom) |
| [ITransformProvider2::get\_ZoomLevel](nf-uiautomationcore-itransformprovider2-get_zoomlevel)   Retrieves the current zoom level of the element. |
| [ITransformProvider2::get\_ZoomMaximum](nf-uiautomationcore-itransformprovider2-get_zoommaximum)   Retrieves the maximum zoom level of the element. |
| [ITransformProvider2::get\_ZoomMinimum](nf-uiautomationcore-itransformprovider2-get_zoomminimum)   Retrieves the minimum zoom level of the element. |
| [ITransformProvider2::Zoom](nf-uiautomationcore-itransformprovider2-zoom)   Zooms the viewport of the control. (ITransformProvider2.Zoom) |
| [ITransformProvider2::ZoomByUnit](nf-uiautomationcore-itransformprovider2-zoombyunit)   Zooms the viewport of the control by the specified logical unit. |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 8 [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2012 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[Control Pattern Interfaces for Providers](/en-us/windows/desktop/WinAuto/uiauto-cpinterfaces)

[ITransformProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-itransformprovider)

---
