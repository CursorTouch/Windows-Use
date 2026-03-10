# get_IsSelectionRequired

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nf-uiautomationcore-iselectionprovider-get_isselectionrequired)

# ISelectionProvider::get\_IsSelectionRequired method (uiautomationcore.h)

Indicates whether the Microsoft UI Automation provider requires at least one child element to be selected.

This property is read-only.

## Syntax

```
HRESULT get_IsSelectionRequired(
  BOOL *pRetVal
);
```

## Parameters

`pRetVal`

## Return value

None

## Remarks

This property can be dynamic. For example, the initial state of a control might
not have any items selected by default, meaning that **ISelectionProvider::IsSelectionRequired** is **FALSE**.
However, after an item is selected the control must always have at least one item selected.

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
