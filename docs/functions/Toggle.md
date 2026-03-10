# Toggle

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nf-uiautomationcore-itoggleprovider-toggle)

# IToggleProvider::Toggle method (uiautomationcore.h)

Cycles through the toggle states of a control.

## Syntax

```
HRESULT Toggle();
```

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

A control must cycle through its [ToggleState](/en-us/windows/desktop/api/uiautomationcore/ne-uiautomationcore-togglestate) in this order:
**ToggleState\_On**, **ToggleState\_Off**
and, if supported, **ToggleState\_Indeterminate**.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2003 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[IToggleProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-itoggleprovider)

[UI Automation Providers Overview](/en-us/windows/desktop/WinAuto/uiauto-providersoverview)

---
