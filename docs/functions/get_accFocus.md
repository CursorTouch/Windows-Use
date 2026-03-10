# get_accFocus

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/oleacc/nf-oleacc-iaccessible-get_accfocus)

# IAccessible::get\_accFocus method (oleacc.h)

The **IAccessible::get\_accFocus** method retrieves the object that has the keyboard focus. All objects that may receive the keyboard focus must support this property.

## Syntax

```
HRESULT get_accFocus(
  [out, retval] VARIANT *pvarChild
);
```

## Parameters

`[out, retval] pvarChild`

Type: **VARIANT\***

Address of a [VARIANT structure](/en-us/windows/desktop/WinAuto/variant-structure) that receives information about the object that has the focus. The following table describes the information returned in *pvarID*.

| Value | Meaning |
| --- | --- |
| **VT\_EMPTY** | None. Neither this object nor any of its children has the keyboard focus. |
| **VT\_I4** | **lVal** is CHILDID\_SELF. The object itself has the keyboard focus. |
| **VT\_I4** | **lVal** contains the child ID of the child element that has the keyboard focus. |
| **VT\_DISPATCH** | **pdispVal** member is the address of the [IDispatch interface](/en-us/windows/desktop/WinAuto/idispatch-interface) for the child object that has the keyboard focus. |

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If successful, returns S\_OK.

If not successful, returns one of the values in the table that follows, or another standard [COM error code](/en-us/windows/desktop/WinAuto/return-values). Servers return these values, but clients must always check output parameters to ensure that they contain valid values. For more information, see [Checking IAccessible Return Values](/en-us/windows/desktop/WinAuto/checking-iaccessible-return-values).

| Error | Description |
| --- | --- |
| **S\_FALSE** | The object is a window but not the foreground window. |
| **DISP\_E\_MEMBERNOTFOUND** | The object does not support this property. |

## Remarks

The concept of keyboard focus is related to that of an active window. An active window is the foreground window on which the user works. The object with the keyboard focus is either the active window or a child object of the active window.

Only one object or item within a container has the focus at any one time. The object with the keyboard focus is not always the selected object. For more information about the difference between selection and focus, see [Selection and Focus Properties and Methods](/en-us/windows/desktop/WinAuto/selection-and-focus-properties-and-methods).

This method returns either an [IDispatch](/en-us/windows/desktop/WinAuto/idispatch-interface) interface pointer or a child ID for the *pvarID*. For more information about how to use the **IDispatch** interface pointer or child ID, see [How Child IDs Are Used in Parameters](/en-us/windows/desktop/WinAuto/how-child-ids-are-used-in-parameters).

As with other [IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible) methods and functions, clients might receive errors for **IAccessible** interface pointers because of a user action. For more information, see [Receiving Errors for IAccessible Interface Pointers](/en-us/windows/desktop/WinAuto/receiving-errors-for-iaccessible-interface-pointers).

### Server Example

The following example code shows a possible implementation of this method for a custom single-selection list box. If the control does not have the focus, VT\_EMPTY is returned in the variant by the standard accessible object for the HWND. If the control does have the focus, and an item is selected, the child ID of that item is returned; if there is no selection, CHILDID\_SELF is returned.

```
// m_pControl is the control object that is served by this implementation. 
// m_pStdAccessibleObject is the object returned by CreateStdAccessibleObject. 

HRESULT STDMETHODCALLTYPE AccServer::get_accFocus(VARIANT *pvarChild)
{
    FAIL_IF_NO_CONTROL;  // Macro that checks for existence of control. 

    HRESULT hr = m_pStdAccessibleObject->get_accFocus(pvarChild);  
    if (pvarChild->vt != VT_I4)
    {
        return hr;
    }
    else
    {
        int index = m_pControl->GetSelectedIndex();
        if (index <0)
        {
            pvarChild->lVal = CHILDID_SELF;
        }
        else
        {
            // Convert to 1-based index for child ID. 
            pvarChild->lVal = index + 1;
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

[IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible)

[IAccessible::accSelect](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccessible-accselect)

[IAccessible::get\_accSelection](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccessible-get_accselection)

[IDispatch](/en-us/windows/desktop/WinAuto/idispatch-interface)

[Selection and Focus Properties and Methods](/en-us/windows/desktop/WinAuto/selection-and-focus-properties-and-methods)

---
