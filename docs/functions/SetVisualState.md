# SetVisualState

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nf-uiautomationcore-iwindowprovider-setvisualstate)

# IWindowProvider::SetVisualState method (uiautomationcore.h)

Changes the visual state of the window. For example, minimizes or maximizes it.

## Syntax

```
HRESULT SetVisualState(
  [in] WindowVisualState state
);
```

## Parameters

`[in] state`

Type: **[WindowVisualState](/en-us/windows/desktop/api/uiautomationcore/ne-uiautomationcore-windowvisualstate)**

The state of the window.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

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

[UI Automation Providers Overview](/en-us/windows/desktop/WinAuto/uiauto-providersoverview)

[WindowVisualState](/en-us/windows/desktop/api/uiautomationcore/nf-uiautomationcore-iwindowprovider-get_windowvisualstate)

---
