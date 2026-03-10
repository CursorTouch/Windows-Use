# get_AutomationElementMode

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationcacherequest-get_automationelementmode)

# IUIAutomationCacheRequest::get\_AutomationElementMode method (uiautomationclient.h)

Indicates whether returned elements contain full references to the underlying UI, or only cached information.

This property is read/write.

## Syntax

```
HRESULT get_AutomationElementMode(
  AutomationElementMode *mode
);
```

## Parameters

`mode`

## Return value

None

## Remarks

[AutomationElementMode\_Full](/en-us/windows/desktop/api/uiautomationclient/ne-uiautomationclient-automationelementmode) is the default value, and specifies that returned elements contain a full reference to the underlying UI. [AutomationElementMode\_None](/en-us/windows/desktop/api/uiautomationclient/ne-uiautomationclient-automationelementmode) specifies that the returned elements have no reference to the underlying UI, and contain only cached information.

Certain operations on elements, including [GetCurrentPropertyValue](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-getcurrentpropertyvalue), and [SetFocus](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-setfocus), require a full reference; attempting to perform these on an element that has none results in an error.

Using [AutomationElementMode\_None](/en-us/windows/desktop/api/uiautomationclient/ne-uiautomationclient-automationelementmode) can be more efficient when only properties are needed, as it avoids the overhead involved in setting up full references.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

---
