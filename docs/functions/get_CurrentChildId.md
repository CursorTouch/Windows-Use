# get_CurrentChildId

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationlegacyiaccessiblepattern-get_currentchildid)

# IUIAutomationLegacyIAccessiblePattern::get\_CurrentChildId method (uiautomationclient.h)

Retrieves the Microsoft Active Accessibility child identifier for the element.

This property is read-only.

## Syntax

```
HRESULT get_CurrentChildId(
  int *pRetVal
);
```

## Parameters

`pRetVal`

## Return value

None

## Remarks

If the element is not a child element, CHILDID\_SELF (0) is returned.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

---
