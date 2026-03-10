# get_accDefaultAction

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/oleacc/nf-oleacc-iaccessible-get_accdefaultaction)

# IAccessible::get\_accDefaultAction method (oleacc.h)

The **IAccessible::get\_accDefaultAction** method retrieves a string that indicates the object's default action. Not all objects have a default action.

## Syntax

```
HRESULT get_accDefaultAction(
  [in]          VARIANT varChild,
  [out, retval] BSTR    *pszDefaultAction
);
```

## Parameters

`[in] varChild`

Type: **VARIANT**

Specifies whether the retrieved default action is performed by the object or of one of the object's child elements. This parameter is either CHILDID\_SELF (to obtain information about the object) or a child ID (to obtain information about the object's child element). For more information about initializing the [VARIANT structure](/en-us/windows/desktop/WinAuto/variant-structure), see [How Child IDs Are Used in Parameters](/en-us/windows/desktop/WinAuto/how-child-ids-are-used-in-parameters).

`[out, retval] pszDefaultAction`

Type: **BSTR\***

Address of a **BSTR** that receives a localized string that describes the default action for the specified object; if this object has no default action, the value is **NULL**.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If successful, returns S\_OK.

If not successful, returns one of the values in the table that follows, or another standard [COM error code](/en-us/windows/desktop/WinAuto/return-values). Servers return these values, but clients must always check output parameters to ensure that they contain valid values. For more information, see [Checking IAccessible Return Values](/en-us/windows/desktop/WinAuto/checking-iaccessible-return-values).

| Error | Description |
| --- | --- |
| **S\_FALSE** | The specified object does not have a default action. |
| **E\_INVALIDARG** | An argument is not valid. |
| **DISP\_E\_MEMBERNOTFOUND** | The specified object does not support this property. |

## Remarks

The retrieved string describes the action that is performed on an object, not what the object does as a result. For example, a toolbar button that prints a document has a default action of "Press" rather than "Prints the current document."

Do not confuse an object's default action with its value. For more information, see [DefaultAction Property](/en-us/windows/desktop/WinAuto/defaultaction-property).

Only controls that perform actions support this method.

**Note to server developers:**Localize the string returned from this property.

### Server Example

The following example code shows a possible implementation of this method for a custom list box. For simplicity, the strings are not localized.

```
HRESULT STDMETHODCALLTYPE AccServer::get_accDefaultAction( 
    VARIANT varChild,
    BSTR *pszDefaultAction)
{
    if (varChild.vt != VT_I4)
    {
        *pszDefaultAction = NULL;
        return E_INVALIDARG;
    }
    if (varChild.lVal == CHILDID_SELF)
    {
        *pszDefaultAction = SysAllocString(L"None.");
    }
    else
    {
        *pszDefaultAction = SysAllocString(L"Double-click");
    }
    return S_OK;
};
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

[DefaultAction Property](/en-us/windows/desktop/WinAuto/defaultaction-property)

[IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible)

[IAccessible::accDoDefaultAction](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccessible-accdodefaultaction)

[VARIANT](/en-us/windows/desktop/WinAuto/variant-structure)

---
