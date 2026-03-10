# get_accSelection

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/oleacc/nf-oleacc-iaccessible-get_accselection)

# IAccessible::get\_accSelection method (oleacc.h)

The **IAccessible::get\_accSelection** method retrieves the selected children of this object. All objects that support selection must support this property.

## Syntax

```
HRESULT get_accSelection(
  [out, retval] VARIANT *pvarChildren
);
```

## Parameters

`[out, retval] pvarChildren`

Type: **VARIANT\***

Address of a [VARIANT structure](/en-us/windows/desktop/WinAuto/variant-structure) that receives information about which children are selected. The following table describes the information returned in *pvarChildren*.

| vt member | Value member |
| --- | --- |
| **VT\_EMPTY** | No children are selected. |
| **VT\_DISPATCH** | One child object is selected, and the address of its [IDispatch](/en-us/windows/desktop/WinAuto/idispatch-interface) interface is set in the **pdispVal** member. |
| **VT\_I4** | **lVal** contains the child ID of the child element that is selected. If **lVal** is CHILDID\_SELF, this means that the object itself is selected. |
| **VT\_UNKNOWN** | Multiple child objects are selected, and the **punkVal** member contains the address of the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. The client queries this interface for the [IEnumVARIANT](/en-us/windows/win32/api/oaidl/nn-oaidl-ienumvariant) interface, which it uses to enumerate the selected objects. |

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If successful, returns S\_OK.

If not successful, returns one of the values in the table that follows, or another standard [COM error code](/en-us/windows/desktop/WinAuto/return-values). Servers return these values, but clients must always check output parameters to ensure that they contain valid values. For more information, see [Checking IAccessible Return Values](/en-us/windows/desktop/WinAuto/checking-iaccessible-return-values).

| Error | Description |
| --- | --- |
| **DISP\_E\_MEMBERNOTFOUND** | The object does not support this property. |

## Remarks

This method must support the [IEnumVARIANT](/en-us/windows/win32/api/oaidl/nn-oaidl-ienumvariant) interface.

This method returns either an [IDispatch](/en-us/windows/desktop/WinAuto/idispatch-interface) interface pointer or a child ID for the *pvarChildren* parameter. For more information about how to use the **IDispatch** interface pointer or child ID, see [How Child IDs Are Used in Parameters](/en-us/windows/desktop/WinAuto/how-child-ids-are-used-in-parameters).

As with other [IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible) methods and functions, clients might receive errors for **IAccessible** interface pointers because of a user action. For more information, see [Receiving Errors for IAccessible Interface Pointers](/en-us/windows/desktop/WinAuto/receiving-errors-for-iaccessible-interface-pointers).

**Note:**This method retrieves a selected item, not selected text.

### Server Example

The following example code shows a possible implementation of this method for a custom single-selection list box. Its **GetSelectedIndex** method returns -1 if no item is selected.

```
// m_pControl is the control that returns this accessible object. 

HRESULT STDMETHODCALLTYPE AccServer::get_accSelection(VARIANT *pvarChildren)
{
    int childID = m_pControl->GetSelectedIndex() + 1; // Convert from 0-based. 
    if (childID <= 0)
    {
        pvarChildren->vt = VT_EMPTY;
    }
    else 
    {
        pvarChildren->vt = VT_I4;
        pvarChildren->lVal = childID;
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

[IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible)

[IAccessible::accSelect](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccessible-accselect)

[IAccessible::get\_accFocus](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccessible-get_accfocus)

[IDispatch](/en-us/windows/desktop/WinAuto/idispatch-interface)

[Selection and Focus Properties and Methods](/en-us/windows/desktop/WinAuto/selection-and-focus-properties-and-methods)

[VARIANT](/en-us/windows/desktop/WinAuto/variant-structure)

---
