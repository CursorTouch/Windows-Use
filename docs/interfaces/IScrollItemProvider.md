# IScrollItemProvider

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nn-uiautomationcore-iscrollitemprovider)

# IScrollItemProvider interface (uiautomationcore.h)

Provides access
to individual child controls of containers that implement [IScrollProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-iscrollprovider).

## Inheritance

The **IScrollItemProvider** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **IScrollItemProvider** also has these types of members:

## Methods

The **IScrollItemProvider** interface has these methods.

|  |
| --- |
| [IScrollItemProvider::ScrollIntoView](nf-uiautomationcore-iscrollitemprovider-scrollintoview)   Scrolls the content area of a container object in order to display the control within the visible region (viewport) of the container. |

## Remarks

Implemented on a Microsoft UI Automation provider that must
support the [ScrollItem](/en-us/windows/desktop/WinAuto/uiauto-implementingscrollitem) control pattern.

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
