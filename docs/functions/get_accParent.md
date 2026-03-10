# get_accParent

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/oleacc/nf-oleacc-iaccessible-get_accparent)

# IAccessible::get\_accParent method (oleacc.h)

The **IAccessible::get\_accParent** method retrieves the [IDispatch](/en-us/windows/desktop/WinAuto/idispatch-interface) of the object's parent. All objects support this property.

## Syntax

```
HRESULT get_accParent(
  [out, retval] IDispatch **ppdispParent
);
```

## Parameters

`[out, retval] ppdispParent`

Type: **IDispatch\*\***

Receives the address of the parent object's [IDispatch](/en-us/windows/desktop/WinAuto/idispatch-interface) interface. If no parent exists or if the child cannot access its parent, the variable is set to **NULL**.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If successful, returns S\_OK.

If not successful, returns one of the values in the table that follows, or another standard [COM error code](/en-us/windows/desktop/WinAuto/return-values). Servers return these values, but clients must always check output parameters to ensure that they contain valid values. For more information, see [Checking IAccessible Return Values](/en-us/windows/desktop/WinAuto/checking-iaccessible-return-values).

| Error | Description |
| --- | --- |
| **S\_FALSE** | No parent exists for this object. |

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

[IAccessible::get\_accChild](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccessible-get_accchild)

[IDispatch](/en-us/windows/desktop/WinAuto/idispatch-interface)

[Object Navigation Properties and Methods](/en-us/windows/desktop/WinAuto/object-navigation-properties-and-methods)

---
