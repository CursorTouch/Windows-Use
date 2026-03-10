# IUIAutomationMultipleViewPattern

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nn-uiautomationclient-iuiautomationmultipleviewpattern)

# IUIAutomationMultipleViewPattern interface (uiautomationclient.h)

Provides access to a control that can switch between multiple representations of the same information or set of child controls.

## Inheritance

The **IUIAutomationMultipleViewPattern** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **IUIAutomationMultipleViewPattern** also has these types of members:

## Methods

The **IUIAutomationMultipleViewPattern** interface has these methods.

|  |
| --- |
| [IUIAutomationMultipleViewPattern::get\_CachedCurrentView](nf-uiautomationclient-iuiautomationmultipleviewpattern-get_cachedcurrentview)   Retrieves the cached control-specific identifier of the current view of the control. |
| [IUIAutomationMultipleViewPattern::get\_CurrentCurrentView](nf-uiautomationclient-iuiautomationmultipleviewpattern-get_currentcurrentview)   Retrieves the control-specific identifier of the current view of the control. |
| [IUIAutomationMultipleViewPattern::GetCachedSupportedViews](nf-uiautomationclient-iuiautomationmultipleviewpattern-getcachedsupportedviews)   Retrieves a collection of control-specific view identifiers from the cache. |
| [IUIAutomationMultipleViewPattern::GetCurrentSupportedViews](nf-uiautomationclient-iuiautomationmultipleviewpattern-getcurrentsupportedviews)   Retrieves a collection of control-specific view identifiers. (IUIAutomationMultipleViewPattern.GetCurrentSupportedViews) |
| [IUIAutomationMultipleViewPattern::GetViewName](nf-uiautomationclient-iuiautomationmultipleviewpattern-getviewname)   Retrieves the name of a control-specific view. (IUIAutomationMultipleViewPattern.GetViewName) |
| [IUIAutomationMultipleViewPattern::SetCurrentView](nf-uiautomationclient-iuiautomationmultipleviewpattern-setcurrentview)   Sets the view of the control. |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[Control Pattern Interfaces for Clients](/en-us/windows/desktop/WinAuto/uiauto-client-controlpatterninterfaces)

---
