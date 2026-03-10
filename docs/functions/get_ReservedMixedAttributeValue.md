# get_ReservedMixedAttributeValue

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomation-get_reservedmixedattributevalue)

# IUIAutomation::get\_ReservedMixedAttributeValue method (uiautomationclient.h)

Retrieves a static token object representing a text attribute that is a mixed attribute.

This property is read-only.

## Syntax

```
HRESULT get_ReservedMixedAttributeValue(
  IUnknown **mixedAttributeValue
);
```

## Parameters

`mixedAttributeValue`

## Return value

None

## Remarks

The object retrieved by **IUIAutomation::ReservedMixedAttributeValue** can be used for comparison with the results from [IUIAutomationTextRange::GetAttributeValue](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationtextrange-getattributevalue) to determine if a text range contains more than one value for a particular text attribute.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[IUIAutomation](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomation)

[UI Automation Text Attributes](/en-us/windows/desktop/WinAuto/uiauto-textattributes)

---
