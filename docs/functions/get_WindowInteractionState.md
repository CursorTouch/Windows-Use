# get_WindowInteractionState

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nf-uiautomationcore-iwindowprovider-get_windowinteractionstate)

# IWindowProvider::get\_WindowInteractionState method (uiautomationcore.h)

Specifies the current state of the window for the purposes of user interaction.

This property is read-only.

## Syntax

```
HRESULT get_WindowInteractionState(
  WindowInteractionState *pRetVal
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

[IWindowProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-iwindowprovider)

[UI Automation Providers Overview](/en-us/windows/desktop/WinAuto/uiauto-providersoverview)

---
