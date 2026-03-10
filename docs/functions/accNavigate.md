# accNavigate

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/oleacc/nf-oleacc-iaccessible-accnavigate)

# IAccessible::accNavigate method (oleacc.h)

The **IAccessible::accNavigate** method traverses to another UI element within a container and retrieves the object. This method is optional.

**Note**  The **accNavigate** method is deprecated and should not be used. Clients should use other methods and properties such as [AccessibleChildren](/en-us/windows/desktop/api/oleacc/nf-oleacc-accessiblechildren), [get\_accChild](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccessible-get_accchild), [get\_accParent](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccessible-get_accparent), and [IEnumVARIANT](/en-us/windows/win32/api/oaidl/nn-oaidl-ienumvariant).

## Syntax

```
HRESULT accNavigate(
  [in]          long    navDir,
  [in]          VARIANT varStart,
  [out, retval] VARIANT *pvarEndUpAt
);
```

## Parameters

`[in] navDir`

Type: **long**

Specifies the direction to navigate. This direction is in *spatial* order, such as left or right, or *logical* order, such as next or previous. This value is one of the [navigation constants](/en-us/windows/desktop/WinAuto/navigation-constants).

`[in] varStart`

Type: **VARIANT**

Specifies whether the starting object of the navigation is the object itself or one of the object's children. This parameter is either CHILDID\_SELF (to start from the object) or a child ID (to start from one of the object's child elements). For more information about initializing the [VARIANT](/en-us/windows/desktop/WinAuto/variant-structure), see [How Child IDs Are Used in Parameters](/en-us/windows/desktop/WinAuto/how-child-ids-are-used-in-parameters).

`[out, retval] pvarEndUpAt`

Type: **VARIANT\***

[out, retval] Address of a [VARIANT](/en-us/windows/desktop/WinAuto/variant-structure) structure that receives information about the destination object. The following table describes the information that is returned in *pvarEnd*.

| vt member | Value member |
| --- | --- |
| **VT\_EMPTY** | None. There was no UI element in the specified direction. |
| **VT\_I4** | **lVal** contains the child ID of the UI element. |
| **VT\_DISPATCH** | **pdispVal** contains the address of the UI element's [IDispatch](/en-us/windows/desktop/WinAuto/idispatch-interface). |

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If successful, returns S\_OK.

If not successful, returns one of the values in the table that follows, or another standard [COM error code](/en-us/windows/desktop/WinAuto/return-values). Servers return these values, but clients must always check output parameters to ensure that they contain valid values. For more information, see [Checking IAccessible Return Values](/en-us/windows/desktop/WinAuto/checking-iaccessible-return-values) and Return Values.

| Error | Description |
| --- | --- |
| **S\_FALSE** | No screen element was found in the specified direction. |
| **DISP\_E\_MEMBERNOTFOUND** | The object does not support this method. |
| **E\_INVALIDARG** | An argument is not valid. |

## Remarks

Navigation, both spatial and logical, is always restricted to the UI elements within a container. With spatial navigation, clients navigate only to a sibling of the starting object (*varStart*). Depending on the navigational flag used with logical navigation, clients navigate to either a child or to a sibling of the starting object.

The **accNavigate** method retrieves UI elements that have a defined screen location, and invisible objects that do not have a defined screen location.

This method does not change the selection or focus. To change the focus or to select an object, use [IAccessible::accSelect](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccessible-accselect).

To prevent looping when traversing screen elements, **accNavigate** returns S\_FALSE with VT\_EMPTY when you specify [NAVDIR\_NEXT](/en-us/windows/desktop/WinAuto/navigation-constants) on the last element, or [NAVDIR\_PREVIOUS](/en-us/windows/desktop/WinAuto/navigation-constants) on the first element.

As with other [IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible) methods and functions, clients might receive errors for **IAccessible** interface pointers because of a user action. For more information, see [Receiving Errors for IAccessible Interface Pointers](/en-us/windows/desktop/WinAuto/receiving-errors-for-iaccessible-interface-pointers).

Some system-defined UI elements such as menus, menu items, and pop-up menus allow navigation to invisible objects. However, other system-defined UI elements do not support this. Servers can choose whether to support navigating to invisible objects and can either skip over or expose them.

Client applications must return post-process return values when using **accNavigate** to navigate between objects. The goal of the post-processing steps is to give clients an [IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible) interface pointer and a child ID so that they can use the **IAccessible** methods and properties for a UI element.

The following tables describe possible scenarios for **IAccessible::accNavigate**, based on the following criteria:

* A defined starting point (whether you are starting with a full object or a simple element)
* The result returned (an [IDispatch](/en-us/windows/desktop/WinAuto/idispatch-interface) or a VT\_I4 child ID)
* The post-processing that client applications will need to perform to have an [IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible) interface pointer and a child ID

For these tables, assume that *startID* and *endID* are VT\_I4 child IDs (simple elements), and *pStartAcc* and *pEndAcc* are VT\_I4 with CHILDID\_SELF (full objects).

This table describes the following NAVDIR\_ flags: NEXT, PREVIOUS, LEFT, RIGHT, UP, and DOWN. For more information about navigation flags, see [Navigation Constants](/en-us/windows/desktop/WinAuto/navigation-constants).

| Starting point | Result returned | Post-processing for the return value |
| --- | --- | --- |
| *pStartAcc, startID* | VT\_I4 *endID* | Call [get\_accChild](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccessible-get_accchild) on *pStartAcc* passing *endID*. Follow normal procedures outlined in **get\_accChild**. |
| *pStartAcc, startID* | VT\_DISPATCH *pEndAcc* | Use the standard procedures for converting an [IDispatch](/en-us/windows/desktop/WinAuto/idispatch-interface) interface pointer to an [IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible) interface pointer for *pEndAcc*. |
| *pStartAcc*, CHILDID\_SELF | VT\_I4 *endID* | Call [get\_accParent](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccessible-get_accparent) on *pStartAcc*, passing CHILDID\_SELF to get the [IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible) interface pointer of the parent for *endID*. Then, call [get\_accChild](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccessible-get_accchild) on that **IAccessible** interface pointer, passing *endID*. Follow normal procedures outlined in **get\_accChild**. |
| *pStartAcc*, CHILDID\_SELF | VT\_DISPATCH *pEndAcc* | Use the standard procedures for converting an [IDispatch](/en-us/windows/desktop/WinAuto/idispatch-interface) interface pointer to an [IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible) interface pointer for *pEndAcc*. |

The following table describes navigation flags [NAVDIR\_FIRSTCHILD](/en-us/windows/desktop/WinAuto/navigation-constants) and [NAVDIR\_LASTCHILD](/en-us/windows/desktop/WinAuto/navigation-constants). It does not include entries for navigating to a first or last child when the starting point is a simple element because simple elements cannot have children.

| Starting point | Result returned | Post-processing for the return value |
| --- | --- | --- |
| *pStartAcc*, CHILDID\_SELF | VT\_I4 *endID* | Call [get\_accChild](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccessible-get_accchild) on *pStartAcc*, passing endID. Follow normal procedures outlined in **get\_accChild**. |
| *pStartAcc*, CHILDID\_SELF | VT\_DISPATCH *pEndAcc* | Use the standard procedures for converting an [IDispatch](/en-us/windows/desktop/WinAuto/idispatch-interface) interface pointer to an [IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible) interface pointer for *pEndAcc*. |

For more information, see [Object Navigation Properties and Methods](/en-us/windows/desktop/WinAuto/object-navigation-properties-and-methods).

### Server Example

The following example shows a possible implementation of the method for a custom list box whose list items are child elements.

```
// m_pControl is the control that returns this accessible object. 
// m_pStdAccessibleObject is the standard accessible object for the window 
//    that contains the control. 

HRESULT STDMETHODCALLTYPE AccServer::accNavigate( 
    long navDir,
    VARIANT varStart,
    VARIANT *pvarEndUpAt)
{
    // Default value. 
    pvarEndUpAt->vt = VT_EMPTY;

    if (varStart.vt != VT_I4)
    {
        return E_INVALIDARG;
    }

    switch (navDir)
    {
    case NAVDIR_FIRSTCHILD:
        if (varStart.lVal == CHILDID_SELF)
        {
            pvarEndUpAt->vt = VT_I4;
            pvarEndUpAt->lVal = 1;
        }
        else  // Starting with child. 
        {
            return S_FALSE;
        }
        break;

    case NAVDIR_LASTCHILD:
        if (varStart.lVal == CHILDID_SELF)
        {
            pvarEndUpAt->vt = VT_I4;
            pvarEndUpAt->lVal = m_pControl->GetCount();
        }
        else  // Starting with child.           
        {
            return S_FALSE;
        }
        break;

    case NAVDIR_NEXT:   
    case NAVDIR_DOWN:
        if (varStart.lVal != CHILDID_SELF)
        {
            pvarEndUpAt->vt = VT_I4;
            pvarEndUpAt->lVal = varStart.lVal + 1;
            // Out of range. 
            if (pvarEndUpAt->lVal > m_pControl->GetCount())
            {
                pvarEndUpAt->vt = VT_EMPTY;
                return S_FALSE;
            }
        }
        else  // Call through to method on standard object. 
        {
            return m_pStdAccessibleObject->accNavigate(navDir, varStart, pvarEndUpAt);
        }
        break;

    case NAVDIR_PREVIOUS:
    case NAVDIR_UP:
        if (varStart.lVal != CHILDID_SELF)
        {
            pvarEndUpAt->vt = VT_I4;
            pvarEndUpAt->lVal = varStart.lVal - 1;
            // Out of range. 
            if (pvarEndUpAt->lVal <1)
            {
                pvarEndUpAt->vt = VT_EMPTY;
                return S_FALSE;
            }
        }
        else  // Call through to method on standard object. 
        {
            return m_pStdAccessibleObject->accNavigate(navDir, varStart, pvarEndUpAt);
        }
        break;

     // Unsupported directions. 
    case NAVDIR_LEFT:
    case NAVDIR_RIGHT:
        if (varStart.lVal == CHILDID_SELF)
        {
            return m_pStdAccessibleObject->accNavigate(navDir, varStart, pvarEndUpAt);
        }
        else 
        {
            pvarEndUpAt->vt = VT_EMPTY;
            return S_FALSE;
        }
        break;
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

[IDispatch](/en-us/windows/desktop/WinAuto/idispatch-interface)

[Object Navigation Properties and Methods](/en-us/windows/desktop/WinAuto/object-navigation-properties-and-methods)

[VARIANT](/en-us/windows/desktop/WinAuto/variant-structure)

---
