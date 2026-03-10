# get_accName

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/oleacc/nf-oleacc-iaccessible-get_accname)

# IAccessible::get\_accName method (oleacc.h)

The **IAccessible::get\_accName** method retrieves the name of the specified object. All objects support this property.

## Syntax

```
HRESULT get_accName(
  [in]          VARIANT varChild,
  [out, retval] BSTR    *pszName
);
```

## Parameters

`[in] varChild`

Type: **VARIANT**

Specifies whether the retrieved name belongs to the object or one of the object's child elements. This parameter is either CHILDID\_SELF (to obtain information about the object) or a child ID (to obtain information about the object's child element). For more information about initializing the [VARIANT structure](/en-us/windows/desktop/WinAuto/variant-structure), see [How Child IDs Are Used in Parameters](/en-us/windows/desktop/WinAuto/how-child-ids-are-used-in-parameters).

`[out, retval] pszName`

Type: **BSTR\***

Address of a **BSTR** that receives a string that contains the specified object's name.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If successful, returns S\_OK.

If not successful, returns one of the values in the table that follows, or another standard [COM error code](/en-us/windows/desktop/WinAuto/return-values). Servers return these values, but clients must always check output parameters to ensure that they contain valid values. For more information, see [Checking IAccessible Return Values](/en-us/windows/desktop/WinAuto/checking-iaccessible-return-values).

| Error | Description |
| --- | --- |
| **S\_FALSE** | The specified object does not have a name. |
| **E\_INVALIDARG** | An argument is not valid. |

## Remarks

Many objects such as icons, menus, check boxes, combo boxes, and other controls have labels that are displayed to users. Any label that is displayed to users is used for the object's name property. For more information, see the [Name Property](/en-us/windows/desktop/WinAuto/name-property).

**Note to server developers:**If you are using menu or button text for the Name property, remove any ampersands (&) marking the keyboard access keys. Provide the access key to the client in response to [IAccessible::get\_accKeyboardShortcut](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccessible-get_acckeyboardshortcut).

Localize the string returned from this property.

### Server Example

The following example shows a possible implementation of this method for a custom list box control that manages its own child elements.

```
// m_pStdAccessibleObject is the standard object returned by CreateStdAccessibleObject. 
// m_pControl is the control object that provides this accessibility object. It maintains
// a zero-based collection of child items. 

HRESULT STDMETHODCALLTYPE AccServer::get_accName( 
    VARIANT varChild,
    BSTR *pszName)
{
    if (varChild.vt != VT_I4)
    {
        *pszName = NULL;
        return E_INVALIDARG;
    }
    // For the control itself, let the standard accessible object return the name 
    // assigned by the application. This is either the "caption" property or, if 
    // there is no caption, the text of any label. 
    if (varChild.lVal == CHILDID_SELF)
    {
        return m_pStdAccessibleObject->get_accName(varChild, pszName);                  
    }
    
    // Else return the name of the item in the list. 
    else
    {
        CustomListControlItem* pItem = m_pControl->GetItemAt(varChild.lVal - 1);
        if (pItem)
        {
            *pszName = SysAllocString(pItem->GetName());        
       
        }
    }
    return S_OK;
};
```

### Client Example

The following example function displays the accessible name of a control.

```
HRESULT PrintName(IAccessible* pAcc, long childId)
{
    if (pAcc == NULL)
    {
        return E_INVALIDARG;
    }
    BSTR bstrName;
    VARIANT varChild;
    varChild.vt = VT_I4;
    varChild.lVal = childId;
    HRESULT hr = pAcc->get_accName(varChild, &bstrName);
    printf("Name: %S ", bstrName);
    SysFreeString(bstrName);
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

[IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible)

[IAccessible::get\_accKeyboardShortcut](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccessible-get_acckeyboardshortcut)

[Name Property](/en-us/windows/desktop/WinAuto/name-property)

[VARIANT](/en-us/windows/desktop/WinAuto/variant-structure)

---
