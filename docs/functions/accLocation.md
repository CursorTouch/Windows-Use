# accLocation

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/oleacc/nf-oleacc-iaccessible-acclocation)

# IAccessible::accLocation method (oleacc.h)

The **IAccessible::accLocation** method retrieves the specified object's current screen location. All visual objects must support this method. Sound objects do not support this method.

## Syntax

```
HRESULT accLocation(
  [out] long    *pxLeft,
  [out] long    *pyTop,
  [out] long    *pcxWidth,
  [out] long    *pcyHeight,
  [in]  VARIANT varChild
);
```

## Parameters

`[out] pxLeft`

Type: **long\***

Address, in physical screen coordinates, of the variable that receives the x-coordinate of the upper-left boundary of the object's location.

`[out] pyTop`

Type: **long\***

Address, in physical screen coordinates, of the variable that receives the y-coordinate of the upper-left boundary of the object's location.

`[out] pcxWidth`

Type: **long\***

Address, in pixels, of the variable that receives the object's width.

`[out] pcyHeight`

Type: **long\***

Address, in pixels, of the variable that receives the object's height.

`[in] varChild`

Type: **VARIANT**

Specifies whether the location that the server returns should be that of the object or that of one of the object's child elements. This parameter is either CHILDID\_SELF (to obtain information about the object) or a child ID (to obtain information about the object's child element). For more information about initializing the [VARIANT structure](/en-us/windows/desktop/WinAuto/variant-structure), see [How Child IDs Are Used in Parameters](/en-us/windows/desktop/WinAuto/how-child-ids-are-used-in-parameters).

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If successful, returns S\_OK. Clients must always check that output parameters contain valid values.

If not successful, returns one of the values in the table that follows, or another standard [COM error code](/en-us/windows/desktop/WinAuto/return-values). For more information, see [Checking IAccessible Return Values](/en-us/windows/desktop/WinAuto/checking-iaccessible-return-values).

| Error | Description |
| --- | --- |
| **DISP\_E\_MEMBERNOTFOUND** | The object does not support this method. |
| **E\_INVALIDARG** | An argument is not valid. |

## Remarks

This method retrieves the object's bounding rectangle. If the object has a non-rectangular shape, then this method returns the smallest rectangle that completely encompasses the entire object region. For non-rectangular objects, the coordinates of the object's bounding rectangle could fail if tested with [IAccessible::accHitTest](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccessible-acchittest). Examples of such non-rectangular objects are list view items in large-icon mode where a single item has a rectangle for the icon and another rectangle for the text of the icon. Because **accLocation** returns a bounding rectangle, not all points in that rectangle will be within the actual bounds of the object. Some points within the bounding rectangle may not be on the object. For more information, see [Navigation Through Hit Testing and Screen Location](/en-us/windows/desktop/WinAuto/navigation-through-hit-testing-and-screen-location).

**Note:**This method returns width and height. If you want the right and bottom coordinates, calculate them using right = left + width, and bottom = top + height.

### Server Example

The following example shows a possible implementation of the method for a custom list box whose list items are child elements. For the list box itself, the call is passed to the standard accessible object, which returns the screen coordinates of the window.

```
// m_pStdAccessibleObject is the standard accessible object for the control window. 
// m_pControl is the object that represents the control. Its GetItemRect method  
//   retrieves the screen coordinates of the specified item in a zero-based collection. 
// 
HRESULT STDMETHODCALLTYPE AccServer::accLocation( 
    long *pxLeft,
    long *pyTop,
    long *pcxWidth,
    long *pcyHeight,
    VARIANT varChild)
{
    *pxLeft = 0;
    *pyTop = 0;
    *pcxWidth = 0;
    *pcyHeight = 0;
    if (varChild.vt != VT_I4)
    {
        return E_INVALIDARG;
    }
    if (varChild.lVal == CHILDID_SELF)
    {
        return m_pStdAccessibleObject->accLocation(pxLeft, pyTop, pcxWidth, pcyHeight, varChild);
    }
    else
    {
        RECT rect;
        if (m_pControl->GetItemRect(varChild.lVal - 1, &rect) == FALSE)
        {
            return E_INVALIDARG;
        }
        else
        {
            *pxLeft = rect.left;
            *pyTop = rect.top;
            *pcxWidth = rect.right - rect.left;
            *pcyHeight = rect.bottom - rect.top;
            return S_OK;        
        }
    }
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

[Active Accessibility and Windows Vista Screen Scaling](/en-us/windows/desktop/WinAuto/active-accessibility-and-windows-vista-screen-scaling)

[IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible)

[IAccessible::accHitTest](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccessible-acchittest)

[Navigation Through Hit Testing and Screen Location](/en-us/windows/desktop/WinAuto/navigation-through-hit-testing-and-screen-location)

[VARIANT](/en-us/windows/desktop/WinAuto/variant-structure)

---
