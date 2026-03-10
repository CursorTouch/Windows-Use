# IUIAutomationTransformPattern2

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nn-uiautomationclient-iuiautomationtransformpattern2)

# IUIAutomationTransformPattern2 interface (uiautomationclient.h)

Extends the [IUIAutomationTransformPattern](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationtransformpattern) interface to enable Microsoft UI Automation clients to programmatically access the viewport zooming functionality of a control.

## Inheritance

The **IUIAutomationTransformPattern2** interface inherits from [IUIAutomationTransformPattern](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationtransformpattern). **IUIAutomationTransformPattern2** also has these types of members:

## Methods

The **IUIAutomationTransformPattern2** interface has these methods.

|  |
| --- |
| [IUIAutomationTransformPattern2::get\_CachedCanZoom](nf-uiautomationclient-iuiautomationtransformpattern2-get_cachedcanzoom)   Retrieves a cached value that indicates whether the control supports zooming of its viewport. |
| [IUIAutomationTransformPattern2::get\_CachedZoomLevel](nf-uiautomationclient-iuiautomationtransformpattern2-get_cachedzoomlevel)   Retrieves the cached zoom level of the control's viewport. |
| [IUIAutomationTransformPattern2::get\_CachedZoomMaximum](nf-uiautomationclient-iuiautomationtransformpattern2-get_cachedzoommaximum)   Retrieves the cached maximum zoom level of the control's viewport. |
| [IUIAutomationTransformPattern2::get\_CachedZoomMinimum](nf-uiautomationclient-iuiautomationtransformpattern2-get_cachedzoomminimum)   Retrieves the cached minimum zoom level of the control's viewport. |
| [IUIAutomationTransformPattern2::get\_CurrentCanZoom](nf-uiautomationclient-iuiautomationtransformpattern2-get_currentcanzoom)   Indicates whether the control supports zooming of its viewport. (IUIAutomationTransformPattern2.get\_CurrentCanZoom) |
| [IUIAutomationTransformPattern2::get\_CurrentZoomLevel](nf-uiautomationclient-iuiautomationtransformpattern2-get_currentzoomlevel)   Retrieves the zoom level of the control's viewport. |
| [IUIAutomationTransformPattern2::get\_CurrentZoomMaximum](nf-uiautomationclient-iuiautomationtransformpattern2-get_currentzoommaximum)   Retrieves the maximum zoom level of the control's viewport. |
| [IUIAutomationTransformPattern2::get\_CurrentZoomMinimum](nf-uiautomationclient-iuiautomationtransformpattern2-get_currentzoomminimum)   Retrieves the minimum zoom level of the control's viewport. |
| [IUIAutomationTransformPattern2::Zoom](nf-uiautomationclient-iuiautomationtransformpattern2-zoom)   Zooms the viewport of the control. (IUIAutomationTransformPattern2.Zoom) |
| [IUIAutomationTransformPattern2::ZoomByUnit](nf-uiautomationclient-iuiautomationtransformpattern2-zoombyunit)   Zooms the viewport of the control by the specified unit. |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 8 [desktop apps only] |
| **Minimum supported server** | Windows Server 2012 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[Control Pattern Interfaces for Clients](/en-us/windows/desktop/WinAuto/uiauto-client-controlpatterninterfaces)

[IUIAutomationTransformPattern](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationtransformpattern)

---
