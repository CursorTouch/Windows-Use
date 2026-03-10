# get_CurrentValue

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationvaluepattern-get_currentvalue)

# IUIAutomationValuePattern::get\_CurrentValue method (uiautomationclient.h)

Retrieves the value of the element.

This property is read-only.

## Syntax

```
HRESULT get_CurrentValue(
  BSTR *retVal
);
```

## Parameters

`retVal`

## Return value

None

## Remarks

Single-line edit controls support programmatic access to their contents through [IUIAutomationValuePattern](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationvaluepattern). However, multiline edit controls do not support this control pattern, and their contents must be retrieved by using [IUIAutomationTextPattern](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationtextpattern).

This property does not support the retrieval of formatting information or substring values. [IUIAutomationTextPattern](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationtextpattern) must be used in these scenarios as well.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[IUIAutomationValuePattern](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationvaluepattern)

---
