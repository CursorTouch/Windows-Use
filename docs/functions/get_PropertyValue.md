# get_PropertyValue

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationpropertycondition-get_propertyvalue)

# IUIAutomationPropertyCondition::get\_PropertyValue method (uiautomationclient.h)

Retrieves the property value that must be matched for the condition to be true.

This property is read-only.

## Syntax

```
HRESULT get_PropertyValue(
  VARIANT *propertyValue
);
```

## Parameters

`propertyValue`

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
