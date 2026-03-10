# IWindowProvider

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nn-uiautomationcore-iwindowprovider)

# IWindowProvider interface (uiautomationcore.h)

Provides
access to the fundamental window-based functionality of a control.

## Inheritance

The **IWindowProvider** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **IWindowProvider** also has these types of members:

## Methods

The **IWindowProvider** interface has these methods.

|  |
| --- |
| [IWindowProvider::Close](nf-uiautomationcore-iwindowprovider-close)   Attempts to close the window. |
| [IWindowProvider::get\_CanMaximize](nf-uiautomationcore-iwindowprovider-get_canmaximize)   Indicates whether the window can be maximized. (IWindowProvider.get\_CanMaximize) |
| [IWindowProvider::get\_CanMinimize](nf-uiautomationcore-iwindowprovider-get_canminimize)   Indicates whether the window can be minimized. (IWindowProvider.get\_CanMinimize) |
| [IWindowProvider::get\_IsModal](nf-uiautomationcore-iwindowprovider-get_ismodal)   Indicates whether the window is modal. (IWindowProvider.get\_IsModal) |
| [IWindowProvider::get\_IsTopmost](nf-uiautomationcore-iwindowprovider-get_istopmost)   Indicates whether the window is the topmost element in the z-order. (IWindowProvider.get\_IsTopmost) |
| [IWindowProvider::get\_WindowInteractionState](nf-uiautomationcore-iwindowprovider-get_windowinteractionstate)   Specifies the current state of the window for the purposes of user interaction. |
| [IWindowProvider::get\_WindowVisualState](nf-uiautomationcore-iwindowprovider-get_windowvisualstate)   Specifies the visual state of the window; that is, whether the window is normal (restored), minimized, or maximized. |
| [IWindowProvider::SetVisualState](nf-uiautomationcore-iwindowprovider-setvisualstate)   Changes the visual state of the window. For example, minimizes or maximizes it. |
| [IWindowProvider::WaitForInputIdle](nf-uiautomationcore-iwindowprovider-waitforinputidle)   Causes the calling code to block for the specified time or until the associated process enters an idle state, whichever completes first. (IWindowProvider.WaitForInputIdle) |

## Remarks

Implemented on a Microsoft UI Automation provider that must support the [Window Control Pattern](/en-us/windows/win32/winauto/uiauto-implementingwindow) control pattern.

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
