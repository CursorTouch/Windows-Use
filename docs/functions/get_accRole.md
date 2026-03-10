# get_accRole

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/oleacc/nf-oleacc-iaccessible-get_accrole)

# IAccessible::get\_accRole method (oleacc.h)

The **IAccessible::get\_accRole** method retrieves information that describes the role of the specified object. All objects support this property.

## Syntax

```
HRESULT get_accRole(
  [in]          VARIANT varChild,
  [out, retval] VARIANT *pvarRole
);
```

## Parameters

`[in] varChild`

Type: **VARIANT**

Specifies whether the retrieved role information belongs to the object or one of the object's child elements. This parameter is either CHILDID\_SELF (to obtain information about the object) or a child ID (to obtain information about the object's child element). For more information about initializing the [VARIANT](/en-us/windows/desktop/WinAuto/variant-structure), see [How Child IDs Are Used in Parameters](/en-us/windows/desktop/WinAuto/how-child-ids-are-used-in-parameters).

`[out, retval] pvarRole`

Type: **VARIANT\***

Address of a [VARIANT](/en-us/windows/desktop/WinAuto/variant-structure) that receives an [object role](/en-us/windows/desktop/WinAuto/object-roles) constant. The **vt** member must be VT\_I4. The **lVal** member receives an object role constant.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If successful, returns S\_OK.

If not successful, returns one of the values in the table that follows, or another standard [COM error code](/en-us/windows/desktop/WinAuto/return-values). Servers return these values, but clients must always check output parameters to ensure that they contain valid values. For more information, see [Checking IAccessible Return Values](/en-us/windows/desktop/WinAuto/checking-iaccessible-return-values).

| Error | Description |
| --- | --- |
| **E\_INVALIDARG** | An argument is not valid. |

## Remarks

Clients call [GetRoleText](/en-us/windows/desktop/api/oleacc/nf-oleacc-getroletexta) to retrieve a localized string that describes the object's role.

**Note to server developers:**You must use the predefined role constants.

### Server Example

The following example code is a possible implementation of this method for a custom list box that maintains its own list items.

```
HRESULT STDMETHODCALLTYPE AccServer::get_accRole( 
    VARIANT varChild,
    VARIANT *pvarRole)
{
    if (varChild.vt != VT_I4)
    {
        pvarRole->vt = VT_EMPTY;
        return E_INVALIDARG;
    }

    pvarRole->vt = VT_I4;

    if (varChild.lVal == CHILDID_SELF)
    {
        pvarRole->lVal = ROLE_SYSTEM_LIST;
    }
    else
    {
        pvarRole->lVal = ROLE_SYSTEM_LISTITEM;
    }
    return S_OK;
};
```

### Client Example

The following example function displays the role of an accessible object or child element.

```
HRESULT PrintRole(IAccessible* pAcc, long childId)
{
    DWORD roleId;
    if (pAcc == NULL)
    {
        return E_INVALIDARG;    
    }
    VARIANT varChild;
    varChild.vt = VT_I4;
    varChild.lVal = childId;
    VARIANT varResult;
    HRESULT hr = pAcc->get_accRole(varChild, &varResult);
    if ((hr == S_OK) && (varResult.vt == VT_I4))
    {
        roleId = varResult.lVal;
        UINT   roleLength;
        LPTSTR lpszRoleString;

        // Get the length of the string. 
        roleLength = GetRoleText(roleId, NULL, 0);

        // Allocate memory for the string. Add one character to 
        // the length you got in the previous call to make room 
        // for the null character. 
        lpszRoleString = (LPTSTR)malloc((roleLength+1) * sizeof(TCHAR));
        if (lpszRoleString != NULL)
        {
            // Get the string. 
            GetRoleText(roleId, lpszRoleString, roleLength + 1);
#ifdef UNICODE
            printf("Role: %S\n", lpszRoleString);
#else
            printf(("Role: %s\n", lpszRoleString);
#endif
            // Free the allocated memory 
            free(lpszRoleString);
        }
        else 
        {
            return E_OUTOFMEMORY;
        }
    }
    return S_OK;
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

[GetRoleText](/en-us/windows/desktop/api/oleacc/nf-oleacc-getroletexta)

[IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible)

[Role Property](/en-us/windows/desktop/WinAuto/role-property)

[VARIANT](/en-us/windows/desktop/WinAuto/variant-structure)

---
