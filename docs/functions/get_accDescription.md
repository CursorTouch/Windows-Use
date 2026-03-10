# get_accDescription

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/oleacc/nf-oleacc-iaccessible-get_accdescription)

# IAccessible::get\_accDescription method (oleacc.h)

The **IAccessible::get\_accDescription** method retrieves a string that describes the visual appearance of the specified object. Not all objects have a description.

**Note**  The Description property is often used incorrectly and is not supported by Microsoft UI Automation. Microsoft Active Accessibility server developers should not use this property. If more information is needed for accessibility and automation scenarios, use the
properties supported by UI Automation elements and control patterns.

## Syntax

```
HRESULT get_accDescription(
  [in]          VARIANT varChild,
  [out, retval] BSTR    *pszDescription
);
```

## Parameters

`[in] varChild`

Type: **VARIANT**

Specifies whether the retrieved description belongs to the object or one of the object's child elements. This parameter is either CHILDID\_SELF (to obtain information about the object) or a child ID (to obtain information about the object's child element). For more information about initializing the [VARIANT structure](/en-us/windows/desktop/WinAuto/variant-structure), see [How Child IDs Are Used in Parameters](/en-us/windows/desktop/WinAuto/how-child-ids-are-used-in-parameters).

`[out, retval] pszDescription`

Type: **BSTR\***

Address of a **BSTR** that receives a localized string that describes the specified object, or **NULL** if this object has no description.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If successful, returns S\_OK.

If not successful, returns one of the values in the table that follows, or another standard [COM error code](/en-us/windows/desktop/WinAuto/return-values). Servers return these values, but clients must always check output parameters to ensure that they contain valid values. For more information, see [Checking IAccessible Return Values](/en-us/windows/desktop/WinAuto/checking-iaccessible-return-values).

| Return code | Description |
| --- | --- |
| **S\_FALSE** | The specified object does not have a description. |
| **E\_INVALIDARG** | An argument is not valid. |
| **DISP\_E\_MEMBERNOTFOUND** | The specified object does not support this property. |

## Remarks

An Microsoft Active Accessibility server can add support for UI Automation by using Direct Annotation, using the [IAccessibleEx](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-iaccessibleex) interface, or by implementing Microsoft Active Accessibility and UI Automation side-by-side with both implementations handling the [WM\_GETOBJECT](/en-us/windows/win32/winauto/wm-getobject) message.

This property provides a textual equivalent of the object for the user. The description should be similar to the text supplied with the ALT attribute in HTML, which is the text that is displayed to describe images for people using text-only browsers. However, some controls use this property to store extra information about the control that is not related to a textual equivalent. For more information about this property, see [Description Property](/en-us/windows/desktop/WinAuto/description-property).

**Note to server developers:**Localize the string returned from this property.

### Server Example

The following example code shows one possible implementation of this method for a custom list box that maintains its own child elements. The example demonstrates the syntax, but remember that a real text-only list box would probably not need to support this property. For simplicity, the strings in the example are not localized.

```
HRESULT STDMETHODCALLTYPE AccServer::get_accDescription( 
    VARIANT varChild,
    BSTR *pszDescription)
{
    if (varChild.vt != VT_I4)
    {
        *pszDescription = NULL;
        return E_INVALIDARG;
    }
    if (varChild.lVal == CHILDID_SELF)
    {
        *pszDescription = SysAllocString(L"List of contacts.");    
            
    }
    else
    {
        *pszDescription = SysAllocString(L"A contact.");           
            
    }
    return S_OK;
};
```

### Client Example

The following example function retrieves the description of the specified accessible object, or a child element, and displays it on the console.

```
HRESULT PrintDescription(IAccessible* pAcc, long child)
{
    VARIANT varObject;
    varObject.vt = VT_I4;
    varObject.lVal = child;
    BSTR bstrDesc;
    HRESULT hr = pAcc->get_accDescription(varObject, &bstrDesc);
    if (hr == S_OK)
    {
        printf("Description: %S\n", bstrDesc);
        SysFreeString(bstrDesc);
    }
    return hr;
}
```

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 2000 Professional [desktop apps only] |
| **Minimum supported server** | Windows Server 2003 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | oleacc.h |
| **Library** | Oleacc.lib |
| **DLL** | Oleacc.dll |
| **Redistributable** | Active Accessibility 1.3 RDK on Windows NT 4.0 with SP6 and later and Windows 95 |

## See also

**Conceptual**

[Description Property](/en-us/windows/desktop/WinAuto/description-property)

[IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible)

[IAccessible::get\_accHelp](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccessible-get_acchelp)

[IAccessible::get\_accName](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccessible-get_accname)

[IAccessible::get\_accValue](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccessible-get_accvalue)

**Reference**

[Using Direct Annotation](/en-us/windows/desktop/WinAuto/using-direct-annotation)

---
