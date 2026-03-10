# UiaGetPropertyValue

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/nf-uiautomationcoreapi-uiagetpropertyvalue)

# UiaGetPropertyValue function (uiautomationcoreapi.h)

**Note**  This function is deprecated. Client applications should use the Microsoft UI Automation Component Object Model (COM) interfaces instead.

Retrieves the value of a UI Automation property.

## Syntax

```
HRESULT UiaGetPropertyValue(
  [in]  HUIANODE   hnode,
  [in]  PROPERTYID propertyId,
  [out] VARIANT    *pValue
);
```

## Parameters

`[in] hnode`

Type: **HUIANODE**

The element that the property is being requested from.

`[in] propertyId`

Type: **PROPERTYID**

The property identifier. For a list of property IDs, see [Property Identifiers](/en-us/windows/desktop/WinAuto/uiauto-entry-propids).

`[out] pValue`

Type: **[VARIANT](/en-us/windows/desktop/WinAuto/variant-structure)\***

Receives the value of the specified property, or the value returned by [UiaGetReservedNotSupportedValue](/en-us/windows/desktop/api/uiautomationcoreapi/nf-uiautomationcoreapi-uiagetreservednotsupportedvalue) if the property is not supported.
This parameter is passed uninitialized.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

Returns S\_OK if successful or an error value otherwise.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps only] |
| **Minimum supported server** | Windows Server 2003 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationcoreapi.h |
| **Library** | Uiautomationcore.lib |
| **DLL** | Uiautomationcore.dll |

---
