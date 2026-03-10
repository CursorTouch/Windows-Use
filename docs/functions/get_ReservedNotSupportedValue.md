# get_ReservedNotSupportedValue

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomation-get_reservednotsupportedvalue)

# IUIAutomation::get\_ReservedNotSupportedValue method (uiautomationclient.h)

Retrieves a static token object representing a property or text attribute that is not supported.

This property is read-only.

## Syntax

```
HRESULT get_ReservedNotSupportedValue(
  IUnknown **notSupportedValue
);
```

## Parameters

`notSupportedValue`

## Return value

None

## Remarks

This object can be used for comparison with the results from [IUIAutomationElement::GetCurrentPropertyValue](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-getcurrentpropertyvalue) or [IUIAutomationTextRange::GetAttributeValue](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationtextrange-getattributevalue).

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[IUIAutomation](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomation)

---
