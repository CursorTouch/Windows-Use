# GetCachedPropertyValue

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-getcachedpropertyvalue)

# IUIAutomationElement::GetCachedPropertyValue method (uiautomationclient.h)

Retrieves a property value from the cache for this UI Automation element.

## Syntax

```
HRESULT GetCachedPropertyValue(
  [in]          PROPERTYID propertyId,
  [out, retval] VARIANT    *retVal
);
```

## Parameters

`[in] propertyId`

Type: **PROPERTYID**

The identifier of the property. For a list of property IDs, see [Property Identifiers](/en-us/windows/desktop/WinAuto/uiauto-entry-propids).

`[out, retval] retVal`

Type: **[VARIANT](/en-us/windows/desktop/api/oaidl/ns-oaidl-variant)\***

Receives the value of the cached property.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

Microsoft UI Automation properties of the **double** type support Not a Number (NaN) values. When retrieving a property of the **double** type, a client can use the [\_isnan](/en-us/previous-versions/visualstudio/visual-studio-6.0/aa298428(v=vs.60)) function to determine whether the property is a NaN value.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

**Conceptual**

[GetCachedPropertyValueEx](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-getcachedpropertyvalueex)

[GetCurrentPropertyValue](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-getcurrentpropertyvalue)

[IUIAutomationElement](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationelement)

**Reference**

[UI Automation Properties Overview](/en-us/windows/desktop/WinAuto/uiauto-propertiesoverview)

---
