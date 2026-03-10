# get_CurrentDescription

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationlegacyiaccessiblepattern-get_currentdescription)

# IUIAutomationLegacyIAccessiblePattern::get\_CurrentDescription method (uiautomationclient.h)

Retrieves the Microsoft Active Accessibility description of the element.

This property is read-only.

## Syntax

```
HRESULT get_CurrentDescription(
  BSTR *pszDescription
);
```

## Parameters

`pszDescription`

## Return value

None

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

---
