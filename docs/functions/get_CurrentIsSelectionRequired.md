# get_CurrentIsSelectionRequired

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationselectionpattern-get_currentisselectionrequired)

# IUIAutomationSelectionPattern::get\_CurrentIsSelectionRequired method (uiautomationclient.h)

Indicates whether at least one item must be selected at all times.

This property is read-only.

## Syntax

```
HRESULT get_CurrentIsSelectionRequired(
  BOOL *retVal
);
```

## Parameters

`retVal`

## Return value

None

## Remarks

This property can be dynamic. For example, the initial state of a control might not have any items selected by default, but after an item is selected, the control must always have at least one item selected.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[IUIAutomationSelectionPattern](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationselectionpattern)

---
