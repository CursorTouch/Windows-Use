# GetPropertyValue

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nf-uiautomationcore-irawelementprovidersimple-getpropertyvalue)

# IRawElementProviderSimple::GetPropertyValue method (uiautomationcore.h)

Retrieves the value of a property supported by the Microsoft UI Automation provider.

## Syntax

```
HRESULT GetPropertyValue(
  [in]          PROPERTYID propertyId,
  [out, retval] VARIANT    *pRetVal
);
```

## Parameters

`[in] propertyId`

Type: **PROPERTYID**

The property identifier. For a list of property IDs, see [Property Identifiers](/en-us/windows/desktop/WinAuto/uiauto-entry-propids).

`[out, retval] pRetVal`

Type: **[VARIANT](/en-us/windows/desktop/WinAuto/variant-structure)\***

Receives the property value, or **VT\_EMPTY** if the property is not supported by this
provider. This parameter is passed uninitialized. See Remarks.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an [HRESULT](/en-us/windows/desktop/WinProg/windows-data-types) error code.

If the provider does not support the *propertyId* property, the provider should set *pRetVal->vt* to **VT\_EMPTY** and return **S\_OK**.

## Remarks

If a provider is explicitly hiding the property value (that is, the provider does not supply the property, and the request is not to be passed through to other providers), it should return a pointer obtained by using the [UiaGetReservedNotSupportedValue](/en-us/windows/desktop/api/uiautomationcoreapi/nf-uiautomationcoreapi-uiagetreservednotsupportedvalue) function. For example:

```
pRetVal->vt = VT_UNKNOWN;
UiaGetReservedNotSupportedValue(&pRetVal->punkVal);
```

UI Automation properties of the **double** type support Not a Number (NaN) values. When returning a NaN value, the provider should return a quiet (non-signaling) NaN to avoid raising an exception if floating-point exceptions are turned on. The following example shows how to create a quiet NaN:

```
ULONGLONG ulNaN = 0xFFFFFFFFFFFFFFFF;
    *pRetVal = *reinterpret_cast<double*>(&ulNaN);
```

Alternatively, you can use the following function from the standard C++ libraries:

```
numeric_limits<double>::quiet_NaN( )
```

#### Examples

The following example returns various property values. The **UiaIds** structure contains
property identifiers; to see how it is initialized, see [UiaLookupId](/en-us/windows/desktop/api/uiautomationcoreapi/nf-uiautomationcoreapi-uialookupid).

```
HRESULT STDMETHODCALLTYPE Provider::GetPropertyValue(PROPERTYID propertyId, 
        VARIANT* pRetVal)
{
    if (propertyId == UiaIds.ControlTypeProperty)
    {
        pRetVal->vt = VT_I4;
        pRetVal->lVal = UiaIds.ButtonControlType;
    }

    // The Name property normally comes from the Caption property of the 
    // control window, if it has one. The Name is overridden here for the 
    // sake of illustration. 
    else if (propertyId == UiaIds.NameProperty)
    {
        pRetVal->vt = VT_BSTR;
        pRetVal->bstrVal = SysAllocString(L"ColorButton");
    }
    else
    {
        pRetVal->vt = VT_EMPTY;
        // UI Automation will attempt to get the property from the host 
        //window provider.
    }
    return S_OK;
}
```

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2003 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[IRawElementProviderSimple](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-irawelementprovidersimple)

---
