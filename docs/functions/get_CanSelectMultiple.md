# get_CanSelectMultiple

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nf-uiautomationcore-iselectionprovider-get_canselectmultiple)

# ISelectionProvider::get\_CanSelectMultiple method (uiautomationcore.h)

Indicates whether the Microsoft UI Automation provider
allows more than one child element to be selected concurrently.

This property is read-only.

## Syntax

```
HRESULT get_CanSelectMultiple(
  BOOL *pRetVal
);
```

## Parameters

`pRetVal`

## Return value

None

## Remarks

This property may be dynamic. For example, in rare cases a control might allow
multiple items to be selected on initialization but subsequently allow only single selections to be made.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2003 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[ISelectionProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-iselectionprovider)

[UI Automation Providers Overview](/en-us/windows/desktop/WinAuto/uiauto-providersoverview)

---
