# IUIAutomationScrollPattern

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nn-uiautomationclient-iuiautomationscrollpattern)

# IUIAutomationScrollPattern interface (uiautomationclient.h)

Provides access to a control that acts as a scrollable container for a collection of child elements. The children of this element support [IUIAutomationScrollItemPattern](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationscrollitempattern).

## Inheritance

The **IUIAutomationScrollPattern** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **IUIAutomationScrollPattern** also has these types of members:

## Methods

The **IUIAutomationScrollPattern** interface has these methods.

|  |
| --- |
| [IUIAutomationScrollPattern::get\_CachedHorizontallyScrollable](nf-uiautomationclient-iuiautomationscrollpattern-get_cachedhorizontallyscrollable)   Retrieves a cached value that indicates whether the element can scroll horizontally. |
| [IUIAutomationScrollPattern::get\_CachedHorizontalScrollPercent](nf-uiautomationclient-iuiautomationscrollpattern-get_cachedhorizontalscrollpercent)   Retrieves the cached horizontal scroll position. |
| [IUIAutomationScrollPattern::get\_CachedHorizontalViewSize](nf-uiautomationclient-iuiautomationscrollpattern-get_cachedhorizontalviewsize)   Retrieves the cached horizontal size of the viewable region of a scrollable element. |
| [IUIAutomationScrollPattern::get\_CachedVerticallyScrollable](nf-uiautomationclient-iuiautomationscrollpattern-get_cachedverticallyscrollable)   Retrieves a cached value that indicates whether the element can scroll vertically. |
| [IUIAutomationScrollPattern::get\_CachedVerticalScrollPercent](nf-uiautomationclient-iuiautomationscrollpattern-get_cachedverticalscrollpercent)   Retrieves the cached vertical scroll position. |
| [IUIAutomationScrollPattern::get\_CachedVerticalViewSize](nf-uiautomationclient-iuiautomationscrollpattern-get_cachedverticalviewsize)   Retrieves the cached vertical size of the viewable region of a scrollable element. |
| [IUIAutomationScrollPattern::get\_CurrentHorizontallyScrollable](nf-uiautomationclient-iuiautomationscrollpattern-get_currenthorizontallyscrollable)   Indicates whether the element can scroll horizontally. |
| [IUIAutomationScrollPattern::get\_CurrentHorizontalScrollPercent](nf-uiautomationclient-iuiautomationscrollpattern-get_currenthorizontalscrollpercent)   Retrieves the horizontal scroll position. |
| [IUIAutomationScrollPattern::get\_CurrentHorizontalViewSize](nf-uiautomationclient-iuiautomationscrollpattern-get_currenthorizontalviewsize)   Retrieves the horizontal size of the viewable region of a scrollable element. |
| [IUIAutomationScrollPattern::get\_CurrentVerticallyScrollable](nf-uiautomationclient-iuiautomationscrollpattern-get_currentverticallyscrollable)   Indicates whether the element can scroll vertically. |
| [IUIAutomationScrollPattern::get\_CurrentVerticalScrollPercent](nf-uiautomationclient-iuiautomationscrollpattern-get_currentverticalscrollpercent)   Retrieves the vertical scroll position. |
| [IUIAutomationScrollPattern::get\_CurrentVerticalViewSize](nf-uiautomationclient-iuiautomationscrollpattern-get_currentverticalviewsize)   Retrieves the vertical size of the viewable region of a scrollable element. |
| [IUIAutomationScrollPattern::Scroll](nf-uiautomationclient-iuiautomationscrollpattern-scroll)   Scrolls the visible region of the content area horizontally and vertically. (IUIAutomationScrollPattern.Scroll) |
| [IUIAutomationScrollPattern::SetScrollPercent](nf-uiautomationclient-iuiautomationscrollpattern-setscrollpercent)   Sets the horizontal and vertical scroll positions as a percentage of the total content area within the UI Automation element. |

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
