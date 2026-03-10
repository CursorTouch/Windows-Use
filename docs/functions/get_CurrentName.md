# get_CurrentName

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationlegacyiaccessiblepattern-get_currentname)

# IUIAutomationLegacyIAccessiblePattern::get\_CurrentName method (uiautomationclient.h)

Retrieves the Microsoft Active Accessibility name property of the element.

This property is read-only.

## Syntax

```
HRESULT get_CurrentName(
  BSTR *pszName
);
```

## Parameters

`pszName`

## Return value

None

## Remarks

The name of an element can be used to find the element in the element tree when the automation ID property is not supported on the element.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

---
