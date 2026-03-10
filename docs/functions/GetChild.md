# GetChild

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationnotcondition-getchild)

# IUIAutomationNotCondition::GetChild method (uiautomationclient.h)

Retrieves the condition of which this condition is the negative.

## Syntax

```
HRESULT GetChild(
  [out, retval] IUIAutomationCondition **condition
);
```

## Parameters

`[out, retval] condition`

Type: **[IUIAutomationCondition](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationcondition)\*\***

Receives a pointer to the condition.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

The returned condition is the one that was used in creating this condition.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[CreateNotCondition](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomation-createnotcondition)

[IUIAutomationNotCondition](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationnotcondition)

---
