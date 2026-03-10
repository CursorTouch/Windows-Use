# accHitTest

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/oleacc/nf-oleacc-iaccessible-acchittest)

# IAccessible::accHitTest method (oleacc.h)

The **IAccessible::accHitTest** method retrieves the child element or child object that is displayed at a specific point on the screen. All visual objects support this method, but sound objects do not. Client applications rarely call this method directly; to get the accessible object that is displayed at a point, use the [AccessibleObjectFromPoint](/en-us/windows/desktop/api/oleacc/nf-oleacc-accessibleobjectfrompoint) function, which calls this method internally.

## Syntax

```
HRESULT accHitTest(
  [in]          long    xLeft,
  [in]          long    yTop,
  [out, retval] VARIANT *pvarChild
);
```

## Parameters

`[in] xLeft`

Type: **long**

Specifies the screen coordinates of the point that is hit tested. The x-coordinates increase from left to right. Note that when screen coordinates are used, the origin is the upper-left corner of the screen.

`[in] yTop`

Type: **long**

Specifies the screen coordinates of the point that is hit tested. The y-coordinates increase from top to bottom. Note that when screen coordinates are used, the origin is the upper-left corner of the screen.

`[out, retval] pvarChild`

Type: **VARIANT\***

[out, retval] Address of a [VARIANT](/en-us/windows/desktop/WinAuto/variant-structure) that identifies the object displayed at the point specified by *xLeft* and *yTop*. The information returned in *pvarID* depends on the location of the specified point in relation to the object whose **accHitTest** method is being called.

| Point location | vt member | Value member |
| --- | --- | --- |
| Outside of the object's boundaries, and either inside or outside of the object's bounding rectangle. | VT\_EMPTY | None. |
| Within the object but not within a child element or a child object. | VT\_I4 | **lVal** is CHILDID\_SELF. |
| Within a child element. | VT\_I4 | **lVal** contains the child ID. |
| Within a child object. | VT\_DISPATCH | *pdispVal* is set to the child object's [IDispatch](/en-us/windows/win32/api/oaidl/nn-oaidl-idispatch) interface pointer |

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If successful, returns S\_OK.

If not successful, returns one of the values in the table that follows, or another standard [COM error code](/en-us/windows/desktop/WinAuto/return-values). Servers return these values, but clients must always check output parameters to ensure that they contain valid values. For more information, see [Checking IAccessible Return Values](/en-us/windows/desktop/WinAuto/checking-iaccessible-return-values).

| Error | Description |
| --- | --- |
| **S\_FALSE** | The point is outside of the object's boundaries. The **vt** member of *pvarID* is VT\_EMPTY. |
| **DISP\_E\_MEMBERNOTFOUND** | The object does not support this method. |
| **E\_INVALIDARG** | An argument is not valid. |

**Note to client developers:**Although servers return S\_FALSE if the **vt** member of *pvarID* is VT\_EMPTY, clients must also handle the case where *pvarID*->vt is VT\_EMPTY and the return value is S\_OK.

## Remarks

If the tested point is on one of the object's children, and this child supports the [IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible) interface itself, this method should return an **IAccessible** interface pointer. However, clients should be prepared to handle an **IAccessible** interface pointer or a child ID. For more information, see [How Child IDs Are Used in Parameters](/en-us/windows/desktop/WinAuto/how-child-ids-are-used-in-parameters).

Because [accLocation](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccessible-acclocation) returns a bounding rectangle, not all points in that rectangle will be within the actual bounds of the object. Some points within the bounding rectangle may not be on the object. For non-rectangular objects, such as list view items in large-icon mode where a single item has a rectangle for the icon and another rectangle for the text of the icon, the coordinates of the object's bounding rectangle retrieved by **IAccessible::accLocation** could fail if tested with **accHitTest** .

As with other [IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible) methods and functions, clients might receive errors for **IAccessible** interface pointers because of a user action. For more information, see [Receiving Errors for IAccessible Interface Pointers](/en-us/windows/desktop/WinAuto/receiving-errors-for-iaccessible-interface-pointers).

When this method is used in certain situations, additional usage notes apply. For more information, see [Navigation Through Hit Testing and Screen Location](/en-us/windows/desktop/WinAuto/navigation-through-hit-testing-and-screen-location).

### Server Example

The following example code shows a possible implementation for a custom list box.

```
// m_pControl is the control that returns this accessible object. 
// m_hwnd is the HWND of the control window. 
//  
HRESULT STDMETHODCALLTYPE AccServer::accHitTest( 
    long xLeft,
    long yTop,
    VARIANT *pvarChild) 

{
    POINT pt;
    pt.x = xLeft;
    pt.y = yTop;

    // Not in our window. 
    if (WindowFromPoint(pt) != m_hwnd)
    {
        pvarChild->vt = VT_EMPTY;
        return S_FALSE;
    }

    else  // In our window; return list item, or self if in blank space. 
    {
        pvarChild->vt = VT_I4;
        ScreenToClient(m_hwnd, &pt);
        // IndexFromY returns the 0-based index of the item at that point, 
        // or -1 if the point is not on any item.
        int index = m_pControl->IndexFromY(pt.y);
        if (index >= 0)
        {
            // Increment, because the child array is 1-based. 
            pvarChild->lVal = index + 1;
        }
        else
        {
            pvarChild->lVal = CHILDID_SELF;

        }
        return S_OK;
    }
};
```

### Client Example

The following example function selects the item at a specified point on the screen within the list represented by *pAcc*. It is assumed that a single selection is wanted.

```
HRESULT SelectItemAtPoint(IAccessible* pAcc, POINT point)
{
    if (pAcc == NULL)
    {
        return E_INVALIDARG;
    }
    VARIANT varChild;

    HRESULT hr = pAcc->accHitTest(point.x, point.y, &varChild);        
    if ((hr == S_OK) && (varChild.lVal != CHILDID_SELF))
    {
        return pAcc->accSelect((SELFLAG_TAKEFOCUS | SELFLAG_TAKESELECTION), varChild);
    }
    return S_FALSE;
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

[Active Accessibility and Windows Vista Screen Scaling](/en-us/windows/desktop/WinAuto/active-accessibility-and-windows-vista-screen-scaling)

[IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible)

[IAccessible::accLocation](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccessible-acclocation)

[IDispatch](/en-us/windows/desktop/WinAuto/idispatch-interface)

[Navigation Through Hit Testing and Screen Location](/en-us/windows/desktop/WinAuto/navigation-through-hit-testing-and-screen-location)

[VARIANT](/en-us/windows/desktop/WinAuto/variant-structure)

---
