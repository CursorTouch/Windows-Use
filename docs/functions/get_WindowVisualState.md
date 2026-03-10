# get_WindowVisualState

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nf-uiautomationcore-iwindowprovider-get_windowvisualstate)

# IWindowProvider::get\_WindowVisualState method (uiautomationcore.h)

Specifies the visual state of the window; that is, whether the window is normal (restored), minimized, or maximized.

This property is read-only.

## Syntax

```
HRESULT get_WindowVisualState(
  WindowVisualState *pRetVal
);
```

## Parameters

`pRetVal`

## Return value

None

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2003 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

**Conceptual**

[IWindowProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-iwindowprovider)

**Reference**

[SetVisualState](/en-us/windows/desktop/api/uiautomationcore/nf-uiautomationcore-iwindowprovider-setvisualstate)

[UI Automation Providers Overview](/en-us/windows/desktop/WinAuto/uiauto-providersoverview)

---
