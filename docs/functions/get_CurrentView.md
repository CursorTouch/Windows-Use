# get_CurrentView

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nf-uiautomationcore-imultipleviewprovider-get_currentview)

# IMultipleViewProvider::get\_CurrentView method (uiautomationcore.h)

Identifies the current view that the control is using to display information or child controls.

This property is read-only.

## Syntax

```
HRESULT get_CurrentView(
  int *pRetVal
);
```

## Parameters

`pRetVal`

## Return value

None

## Remarks

The collection of view identifiers must be identical for all instances of a control.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2003 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |
| **DLL** | Uiautomationcore.dll |

## See also

[IMultipleViewProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-imultipleviewprovider)

[UI Automation Providers Overview](/en-us/windows/desktop/WinAuto/uiauto-providersoverview)

---
