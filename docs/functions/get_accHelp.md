# get_accHelp

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/oleacc/nf-oleacc-iaccessible-get_acchelp)

# IAccessible::get\_accHelp method (oleacc.h)

The **IAccessible::get\_accHelp** method retrieves the **Help** property string of an object. Not all objects support this property.

## Syntax

```
HRESULT get_accHelp(
  [in]          VARIANT varChild,
  [out, retval] BSTR    *pszHelp
);
```

## Parameters

`[in] varChild`

Type: **VARIANT**

Specifies whether the retrieved help information belongs to the object or one of the object's child elements. This parameter is either CHILDID\_SELF (to obtain information about the object) or a child ID (to obtain information about one of the object's child elements). For more information about initializing the [VARIANT](/en-us/windows/desktop/WinAuto/variant-structure), see [How Child IDs Are Used in Parameters](/en-us/windows/desktop/WinAuto/how-child-ids-are-used-in-parameters).

`[out, retval] pszHelp`

Type: **BSTR\***

Address of a **BSTR** that receives the localized string containing the help information for the specified object, or **NULL** if no help information is available.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If successful, returns S\_OK.

If not successful, returns one of the values in the table that follows, or another standard [COM error code](/en-us/windows/desktop/WinAuto/return-values). Servers return these values, but clients must always check output parameters to ensure that they contain valid values. For more information, see [Checking IAccessible Return Values](/en-us/windows/desktop/WinAuto/checking-iaccessible-return-values).

| Error | Description |
| --- | --- |
| **S\_FALSE** | No help information is available. |
| **E\_INVALIDARG** | An argument is not valid. |
| **DISP\_E\_MEMBERNOTFOUND** | The object does not support this property. |

## Remarks

None of the predefined and common controls support this property.

**Note to server developers:**Localize the string returned from this property.

This property returns a string, whereas [IAccessible::get\_accHelpTopic](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccessible-get_acchelptopic) provides access to a Help topic in [WinHelp](/en-us/windows/win32/api/winuser/nf-winuser-winhelpa). Objects are not required to support both **IAccessible::get\_accHelp** and **IAccessible::get\_accHelpTopic**, but they must support at least one. If they easily return a string, they must support **IAccessible::get\_accHelp** ; otherwise they must support **IAccessible::get\_accHelpTopic**. If both are supported, **IAccessible::get\_accHelpTopic** provides more detailed information.

### Server Example

The following example code shows one possible implementation of this method for a custom list box. Different text is displayed depending on the status of the contact in the list. For simplicity, the example does not localize the returned string.

```
// m_pControl is the custom control that returns this accessible object. 
// 'online' is an enumerated value. 

HRESULT STDMETHODCALLTYPE AccServer::get_accHelp( 
    VARIANT varChild,
    BSTR *pszHelp)
{
    *pszHelp = NULL;
    if (varChild.vt != VT_I4)
    {
        return E_INVALIDARG;
    }
    if (varChild.lVal == CHILDID_SELF)
    {
        *pszHelp = SysAllocString(L"Contact list.");
    }
    else
    {
        int index = (int)varChild.lVal - 1;
        CustomListControlItem* pItem = m_pControl->GetItemAt(index);
        if (pItem == NULL)
        {
            return E_INVALIDARG;
        }
        if (pItem->GetStatus() == online)
        {
            *pszHelp = SysAllocString(L"Online contact.");
        }
        else 
        {
            *pszHelp = SysAllocString(L"Offline contact.");
        }
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

[Help Property](/en-us/windows/desktop/WinAuto/help-property)

[IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible)

[IAccessible::get\_accDescription](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccessible-get_accdescription)

[IAccessible::get\_accHelpTopic](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccessible-get_acchelptopic)

[VARIANT](/en-us/windows/desktop/WinAuto/variant-structure)

---
