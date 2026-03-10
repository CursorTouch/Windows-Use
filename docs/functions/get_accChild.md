# get_accChild

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/oleacc/nf-oleacc-iaccessible-get_accchild)

# IAccessible::get\_accChild method (oleacc.h)

The **IAccessible::get\_accChild** method retrieves an [IDispatch](/en-us/windows/desktop/WinAuto/idispatch-interface) for the specified child, if one exists. All objects must support this property.

## Syntax

```
HRESULT get_accChild(
  [in]          VARIANT   varChild,
  [out, retval] IDispatch **ppdispChild
);
```

## Parameters

`[in] varChild`

Type: **VARIANT**

Identifies the child whose [IDispatch](/en-us/windows/desktop/WinAuto/idispatch-interface) interface is retrieved. For more information about initializing the [VARIANT](/en-us/windows/desktop/WinAuto/variant-structure), see [How Child IDs Are Used in Parameters](/en-us/windows/desktop/WinAuto/how-child-ids-are-used-in-parameters).

`[out, retval] ppdispChild`

Type: **IDispatch\*\***

[out, retval] Receives the address of the child object's [IDispatch](/en-us/windows/desktop/WinAuto/idispatch-interface) interface.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If successful, returns S\_OK.

If not successful, returns one of the values in the table that follows, or another standard [COM error code](/en-us/windows/desktop/WinAuto/return-values). Servers return these values, but clients must always check output parameters to ensure that they contain valid values. For more information, see [Checking IAccessible Return Values](/en-us/windows/desktop/WinAuto/checking-iaccessible-return-values).

| Error | Description |
| --- | --- |
| **S\_FALSE** | The child is not an accessible object. |
| **E\_INVALIDARG** | An argument is not valid. |

## Remarks

Servers expose elements as either elements (child IDs) or full objects ([IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible) interface pointers). If a child is an element, **get\_accChild** returns S\_FALSE, and the parent will provide information for that child. If the child is a full object, **get\_accChild** will return the **IAccessible** interface pointer and the parent will not provide information about that child. If **get\_accChild** fails because the server application cannot create an accessible object due to a temporary system error (such as an out-of-memory error), the server should return a suitable failure code.

**Note to server developers:**If *varChildID* contains VT\_EMPTY, you should return E\_INVALIDARG.

### Server Example

The following example code shows an implementation for an object that does not have any children, or whose children are elements rather than objects.

```
HRESULT STDMETHODCALLTYPE AccServer::get_accChild( 
    VARIANT varChild,
    IDispatch **ppdispChild)
{
    if (varChild.vt != VT_I4)
    {
        *ppdispChild = NULL;
        return E_INVALIDARG;
    }
    *ppdispChild = NULL;    
    return S_FALSE;     
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

[AccessibleChildren](/en-us/windows/desktop/api/oleacc/nf-oleacc-accessiblechildren)

[IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible)

[IAccessible::get\_accParent](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccessible-get_accparent)

[IDispatch](/en-us/windows/desktop/WinAuto/idispatch-interface)

[Object Navigation Properties and Methods](/en-us/windows/desktop/WinAuto/object-navigation-properties-and-methods)

[VARIANT](/en-us/windows/desktop/WinAuto/variant-structure)

---
