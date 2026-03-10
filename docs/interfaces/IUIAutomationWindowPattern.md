# IUIAutomationWindowPattern

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nn-uiautomationclient-iuiautomationwindowpattern)

# IUIAutomationWindowPattern interface (uiautomationclient.h)

Provides access to the fundamental functionality of a window.

## Inheritance

The **IUIAutomationWindowPattern** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **IUIAutomationWindowPattern** also has these types of members:

## Methods

The **IUIAutomationWindowPattern** interface has these methods.

|  |
| --- |
| [IUIAutomationWindowPattern::Close](nf-uiautomationclient-iuiautomationwindowpattern-close)   Closes the window. |
| [IUIAutomationWindowPattern::get\_CachedCanMaximize](nf-uiautomationclient-iuiautomationwindowpattern-get_cachedcanmaximize)   Retrieves a cached value that indicates whether the window can be maximized. |
| [IUIAutomationWindowPattern::get\_CachedCanMinimize](nf-uiautomationclient-iuiautomationwindowpattern-get_cachedcanminimize)   Retrieves a cached value that indicates whether the window can be minimized. |
| [IUIAutomationWindowPattern::get\_CachedIsModal](nf-uiautomationclient-iuiautomationwindowpattern-get_cachedismodal)   Retrieves a cached value that indicates whether the window is modal. |
| [IUIAutomationWindowPattern::get\_CachedIsTopmost](nf-uiautomationclient-iuiautomationwindowpattern-get_cachedistopmost)   Retrieves a cached value that indicates whether the window is the topmost element in the z-order. |
| [IUIAutomationWindowPattern::get\_CachedWindowInteractionState](nf-uiautomationclient-iuiautomationwindowpattern-get_cachedwindowinteractionstate)   Retrieves a cached value that indicates the current state of the window for the purposes of user interaction. |
| [IUIAutomationWindowPattern::get\_CachedWindowVisualState](nf-uiautomationclient-iuiautomationwindowpattern-get_cachedwindowvisualstate)   Retrieves a cached value that indicates the visual state of the window; that is, whether it is in the normal, maximized, or minimized state. |
| [IUIAutomationWindowPattern::get\_CurrentCanMaximize](nf-uiautomationclient-iuiautomationwindowpattern-get_currentcanmaximize)   Indicates whether the window can be maximized. (IUIAutomationWindowPattern.get\_CurrentCanMaximize) |
| [IUIAutomationWindowPattern::get\_CurrentCanMinimize](nf-uiautomationclient-iuiautomationwindowpattern-get_currentcanminimize)   Indicates whether the window can be minimized. (IUIAutomationWindowPattern.get\_CurrentCanMinimize) |
| [IUIAutomationWindowPattern::get\_CurrentIsModal](nf-uiautomationclient-iuiautomationwindowpattern-get_currentismodal)   Indicates whether the window is modal. (IUIAutomationWindowPattern.get\_CurrentIsModal) |
| [IUIAutomationWindowPattern::get\_CurrentIsTopmost](nf-uiautomationclient-iuiautomationwindowpattern-get_currentistopmost)   Indicates whether the window is the topmost element in the z-order. (IUIAutomationWindowPattern.get\_CurrentIsTopmost) |
| [IUIAutomationWindowPattern::get\_CurrentWindowInteractionState](nf-uiautomationclient-iuiautomationwindowpattern-get_currentwindowinteractionstate)   Retrieves the current state of the window for the purposes of user interaction. |
| [IUIAutomationWindowPattern::get\_CurrentWindowVisualState](nf-uiautomationclient-iuiautomationwindowpattern-get_currentwindowvisualstate)   Retrieves the visual state of the window; that is, whether it is in the normal, maximized, or minimized state. |
| [IUIAutomationWindowPattern::SetWindowVisualState](nf-uiautomationclient-iuiautomationwindowpattern-setwindowvisualstate)   Minimizes, maximizes, or restores the window. |
| [IUIAutomationWindowPattern::WaitForInputIdle](nf-uiautomationclient-iuiautomationwindowpattern-waitforinputidle)   Causes the calling code to block for the specified time or until the associated process enters an idle state, whichever completes first. (IUIAutomationWindowPattern.WaitForInputIdle) |

## Remarks

Examples of controls that support this control pattern include top-level application windows, multiple-document interface (MDI) child windows, and modal dialog boxes.

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
