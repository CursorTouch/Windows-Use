# IUIAutomationElement2

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nn-uiautomationclient-iuiautomationelement2)

# IUIAutomationElement2 interface (uiautomationclient.h)

Extends the [IUIAutomationElement](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationelement) interface.

## Inheritance

The **IUIAutomationElement2** interface inherits from the IUIAutomationElement interface.

## Methods

The **IUIAutomationElement2** interface has these methods.

|  |
| --- |
| [IUIAutomationElement2::get\_CachedFlowsFrom](nf-uiautomationclient-iuiautomationelement2-get_cachedflowsfrom)   Retrieves a cached array of elements that indicate the reading order before the current element. |
| [IUIAutomationElement2::get\_CachedLiveSetting](nf-uiautomationclient-iuiautomationelement2-get_cachedlivesetting)   Retrieves a cached value that indicates the type of notifications, if any, that the element sends when the content of the element changes. |
| [IUIAutomationElement2::get\_CachedOptimizeForVisualContent](nf-uiautomationclient-iuiautomationelement2-get_cachedoptimizeforvisualcontent)   Retrieves a cached value that indicates whether the provider exposes only elements that are visible. |
| [IUIAutomationElement2::get\_CurrentFlowsFrom](nf-uiautomationclient-iuiautomationelement2-get_currentflowsfrom)   Retrieves an array of elements that indicates the reading order before the current element. |
| [IUIAutomationElement2::get\_CurrentLiveSetting](nf-uiautomationclient-iuiautomationelement2-get_currentlivesetting)   Indicates the type of notifications, if any, that the element sends when the content of the element changes. |
| [IUIAutomationElement2::get\_CurrentOptimizeForVisualContent](nf-uiautomationclient-iuiautomationelement2-get_currentoptimizeforvisualcontent)   Indicates whether the provider exposes only elements that are visible. |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 8 [desktop apps only] |
| **Minimum supported server** | Windows Server 2012 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[IUIAutomationElement](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationelement)

[UI Automation Element Interfaces for Clients](/en-us/windows/desktop/WinAuto/uiauto-entry-uiautoclientinterfaces)

---
