# IScrollProvider

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nn-uiautomationcore-iscrollprovider)

# IScrollProvider interface (uiautomationcore.h)

Provides access
to controls that act as scrollable containers for a collection of child objects.
The children of this control must implement [IScrollItemProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-iscrollitemprovider).

## Inheritance

The **IScrollProvider** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **IScrollProvider** also has these types of members:

## Methods

The **IScrollProvider** interface has these methods.

|  |
| --- |
| [IScrollProvider::get\_HorizontallyScrollable](nf-uiautomationcore-iscrollprovider-get_horizontallyscrollable)   Indicates whether the control can scroll horizontally. |
| [IScrollProvider::get\_HorizontalScrollPercent](nf-uiautomationcore-iscrollprovider-get_horizontalscrollpercent)   Specifies the horizontal scroll position. |
| [IScrollProvider::get\_HorizontalViewSize](nf-uiautomationcore-iscrollprovider-get_horizontalviewsize)   Specifies the horizontal size of the viewable region. |
| [IScrollProvider::get\_VerticallyScrollable](nf-uiautomationcore-iscrollprovider-get_verticallyscrollable)   Indicates whether the control can scroll vertically. |
| [IScrollProvider::get\_VerticalScrollPercent](nf-uiautomationcore-iscrollprovider-get_verticalscrollpercent)   Specifies the vertical scroll position. |
| [IScrollProvider::get\_VerticalViewSize](nf-uiautomationcore-iscrollprovider-get_verticalviewsize)   Specifies the vertical size of the viewable region. |
| [IScrollProvider::Scroll](nf-uiautomationcore-iscrollprovider-scroll)   Scrolls the visible region of the content area horizontally and vertically. (IScrollProvider.Scroll) |
| [IScrollProvider::SetScrollPercent](nf-uiautomationcore-iscrollprovider-setscrollpercent)   Sets the horizontal and vertical scroll position as a percentage of the total content area within the control. |

## Remarks

Implemented on a Microsoft UI Automation provider that must
support the [Scroll](/en-us/windows/desktop/WinAuto/uiauto-implementingscroll) control pattern.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2003 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[UI Automation Providers Overview](/en-us/windows/desktop/WinAuto/uiauto-providersoverview)

---
