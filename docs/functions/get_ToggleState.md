# get_ToggleState

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nf-uiautomationcore-itoggleprovider-get_togglestate)

# IToggleProvider::get\_ToggleState method (uiautomationcore.h)

Specifies the toggle state of the control.

This property is read-only.

## Syntax

```
HRESULT get_ToggleState(
  ToggleState *pRetVal
);
```

## Parameters

`pRetVal`

## Return value

None

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
