# RegisterProperty

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nf-uiautomationcore-iuiautomationregistrar-registerproperty)

# IUIAutomationRegistrar::RegisterProperty method (uiautomationcore.h)

Registers a third-party property.

## Syntax

```
HRESULT RegisterProperty(
  [in]  const UIAutomationPropertyInfo *property,
  [out] PROPERTYID                     *propertyId
);
```

## Parameters

`[in] property`

Type: **[UIAutomationPropertyInfo](/en-us/windows/desktop/api/uiautomationcore/ns-uiautomationcore-uiautomationpropertyinfo)\***

A pointer to a structure that contains information about the property to register.

`[out] propertyId`

Type: **PropertyID\***

Receives the property ID of the newly registered property.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

The property ID can be used in various property methods, including [GetCurrentPropertyValue](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-getcurrentpropertyvalue), and [CreatePropertyCondition](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomation-createpropertycondition). The same value can be used as a WinEvent value for property change events in [IAccessibleEx](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-iaccessibleex) implementations.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[IUIAutomationRegistrar](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-iuiautomationregistrar)

---
