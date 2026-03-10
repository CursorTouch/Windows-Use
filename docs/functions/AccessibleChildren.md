# AccessibleChildren

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/oleacc/nf-oleacc-accessiblechildren)

# AccessibleChildren function (oleacc.h)

Retrieves the child ID or [IDispatch](/en-us/windows/desktop/WinAuto/idispatch-interface) of each child within an accessible container object.

## Syntax

```
HRESULT AccessibleChildren(
  [in]  IAccessible *paccContainer,
  [in]  LONG        iChildStart,
  [in]  LONG        cChildren,
  [out] VARIANT     *rgvarChildren,
  [out] LONG        *pcObtained
);
```

## Parameters

`[in] paccContainer`

Type: **IAccessible\***

Pointer to the container object's [IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible) interface.

`[in] iChildStart`

Type: **[LONG](/en-us/windows/desktop/WinProg/windows-data-types)**

Specifies the zero-based index of the first child that is retrieved. This parameter is an index, not a child ID, and it is usually is set to zero (0).

`[in] cChildren`

Type: **[LONG](/en-us/windows/desktop/WinProg/windows-data-types)**

Specifies the number of children to retrieve. To retrieve the current number of children, an application calls [IAccessible::get\_accChildCount](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccessible-get_accchildcount).

`[out] rgvarChildren`

Type: **[VARIANT](/en-us/windows/desktop/WinAuto/variant-structure)\***

Pointer to an array of [VARIANT](/en-us/windows/desktop/WinAuto/variant-structure) structures that receives information about the container's children. If the **vt** member of an array element is VT\_I4, then the **lVal** member for that element is the child ID. If the **vt** member of an array element is VT\_DISPATCH, then the **pdispVal** member for that element is the address of the child object's [IDispatch](/en-us/windows/desktop/WinAuto/idispatch-interface) interface.

`[out] pcObtained`

Type: **[LONG](/en-us/windows/desktop/WinProg/windows-data-types)\***

Address of a variable that receives the number of elements in the *rgvarChildren* array that is populated by the **AccessibleChildren** function. This value is the same as that of the *cChildren* parameter; however, if you request more children than exist, this value will be less than that of *cChildren*.

## Return value

Type: **STDAPI**

If successful, returns S\_OK.

If not successful, returns one of the following or another standard [COM error code](/en-us/windows/desktop/WinAuto/return-values).

| Return code | Description |
| --- | --- |
| **E\_INVALIDARG** | An argument is not valid. |
| **S\_FALSE** | The function succeeded, but there are fewer elements in the *rgvarChildren* array than there are children requested in *cChildren*. |

## Remarks

To retrieve information about all of the children in a container, the *iChildStart* parameter must be zero (0), and *cChildren* must be the value returned by [IAccessible::get\_accChildCount](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccessible-get_accchildcount).

When calling this function to obtain information about the children of a user interface element, it is recommended that clients obtain information about all of the children. For example, *iChildStart* must be zero (0), and *cChildren* must be the value returned by [IAccessible::get\_accChildCount](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccessible-get_accchildcount).

If a child ID is returned for an element, then the container must provide information about the child element. To obtain information about the element, clients use the container's [IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible) interface pointer and specify the obtained child ID in calls to the **IAccessible** properties.

Clients must call the [IUnknown::Release](/en-us/windows/win32/api/unknwn/nf-unknwn-iunknown-release) method for any [IDispatch](/en-us/windows/desktop/WinAuto/idispatch-interface) interfaces retrieved by this function, and free the array when it is no longer required.

#### Examples

The following example function displays a view of the element tree below the element that is passed in. The name and role of each element are printed by user-defined functions that are not shown here.

```
HRESULT WalkTreeWithAccessibleChildren(IAccessible* pAcc, int depth)
{
    HRESULT hr;
    long childCount;
    long returnCount;

    if (!pAcc)
    {
        return E_INVALIDARG;
    }
    hr = pAcc->get_accChildCount(&childCount);
    if (FAILED(hr))
    {
        return hr;
    };
    if (childCount == 0)
    {
        return S_FALSE;
    }
    VARIANT* pArray = new VARIANT[childCount];
    hr = AccessibleChildren(pAcc, 0L, childCount, pArray, &returnCount);
    if (FAILED(hr))
    {
        return hr;
    };

    // Iterate through children.
    for (int x = 0; x < returnCount; x++)
    {
        VARIANT vtChild = pArray[x];
        // If it's an accessible object, get the IAccessible, and recurse.
        if (vtChild.vt == VT_DISPATCH)
        {
            IDispatch* pDisp = vtChild.pdispVal;
            IAccessible* pChild = NULL;
            hr = pDisp->QueryInterface(IID_IAccessible, (void**) &pChild);
            if (hr == S_OK)
            {
                for (int y = 0; y < depth; y++)
                {
                    printf("  ");
                }
                PrintName(pChild, CHILDID_SELF);
                printf("(Object) ");
                PrintRole(pChild, CHILDID_SELF);
                WalkTreeWithAccessibleChildren(pChild, depth + 1);
                pChild->Release();
            }
            pDisp->Release();
        }
        // Else it's a child element so we have to call accNavigate on the parent,
        //   and we do not recurse because child elements can't have children.
        else
        {
            for (int y = 0; y < depth; y++)
            {
                printf("  ");
            }
            PrintName(pAcc, vtChild.lVal);
            printf("(Child element) ");
            PrintRole(pAcc, vtChild.lVal);
        }
    }
    delete[] pArray;
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

[IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible)

[IDispatch](/en-us/windows/desktop/WinAuto/idispatch-interface)

[VARIANT](/en-us/windows/desktop/WinAuto/variant-structure)

---
