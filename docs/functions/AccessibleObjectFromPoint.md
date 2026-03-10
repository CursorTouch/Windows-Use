# AccessibleObjectFromPoint

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/oleacc/nf-oleacc-accessibleobjectfrompoint)

# AccessibleObjectFromPoint function (oleacc.h)

Retrieves the address of the [IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible) interface pointer for the object displayed at a specified point on the screen.

## Syntax

```
HRESULT AccessibleObjectFromPoint(
  [in]  POINT       ptScreen,
  [out] IAccessible **ppacc,
  [out] VARIANT     *pvarChild
);
```

## Parameters

`[in] ptScreen`

Specifies, in physical screen coordinates, the point that is examined.

`[out] ppacc`

Address of a pointer variable that receives the address of the object's [IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible) interface.

`[out] pvarChild`

Address of a [VARIANT](/en-us/windows/desktop/WinAuto/variant-structure) structure that specifies whether the [IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible) interface pointer that is returned in *ppacc* belongs to the object displayed at the specified point, or to the parent of the element at the specified point. The **vt** member of the **VARIANT** is always VT\_I4. If the **lVal** member is CHILDID\_SELF, then the **IAccessible** interface pointer at *ppacc* belongs to the object at the point. If the **lVal** member is not CHILDID\_SELF, *ppacc* is the address of the **IAccessible** interface of the child element's parent object. Clients must call [VariantClear](/en-us/previous-versions/windows/desktop/api/oleauto/nf-oleauto-variantclear) on the retrieved **VARIANT** parameter when finished using it.

## Return value

If successful, returns S\_OK.

If not successful, returns one of the following or another standard [COM error code](/en-us/windows/desktop/WinAuto/return-values).

| Return code | Description |
| --- | --- |
| **E\_INVALIDARG** | An argument is not valid. |

## Remarks

This function retrieves the lowest-level accessible object in the object hierarchy at a given point. If the element at the point is not an accessible object (that is, does not support [IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible)), then the function retrieves the **IAccessible** interface of the parent object. The parent object must provide information about the child element through the **IAccessible** interface. Call [IAccessible::accHitTest](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccessible-acchittest) to identify the child element at the specified screen coordinates.

As with other [IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible) methods and functions, clients might receive errors for **IAccessible** interface pointers because of a user action. For more information, see [Receiving Errors for IAccessible Interface Pointers](/en-us/windows/desktop/WinAuto/receiving-errors-for-iaccessible-interface-pointers).

### Client Example

The following example function selects the item at a specified point on the screen. It is assumed that a single selection is wanted.

```
HRESULT SelectItemAtPoint(POINT point)
{
    VARIANT varItem;
    IAccessible* pAcc;
    HRESULT hr = AccessibleObjectFromPoint(point, &pAcc, &varItem);
    if ((hr == S_OK))
    {
        hr = pAcc->accSelect((SELFLAG_TAKEFOCUS | SELFLAG_TAKESELECTION), varItem);
        VariantClear(&varItem);
        pAcc->Release();
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

[AccessibleObjectFromEvent](/en-us/windows/desktop/api/oleacc/nf-oleacc-accessibleobjectfromevent)

[AccessibleObjectFromWindow](/en-us/windows/desktop/api/oleacc/nf-oleacc-accessibleobjectfromwindow)

[Active Accessibility and Windows Vista Screen Scaling](/en-us/windows/desktop/WinAuto/active-accessibility-and-windows-vista-screen-scaling)

[IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible)

[VARIANT Structure](/en-us/windows/desktop/WinAuto/variant-structure)

---
