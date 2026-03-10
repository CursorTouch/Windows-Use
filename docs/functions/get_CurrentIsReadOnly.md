# get_CurrentIsReadOnly

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationvaluepattern-get_currentisreadonly)

# IUIAutomationValuePattern::get\_CurrentIsReadOnly method (uiautomationclient.h)

Indicates whether the value of the element is read-only.

This property is read-only.

## Syntax

```
HRESULT get_CurrentIsReadOnly(
  BOOL *retVal
);
```

## Parameters

`retVal`

## Return value

None

## Remarks

This property must be **TRUE** for [IUIAutomationValuePattern::SetValue](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationvaluepattern-setvalue) to succeed.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

---
