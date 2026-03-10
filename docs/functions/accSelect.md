# accSelect

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/oleacc/nf-oleacc-iaccessible-accselect)

# IAccessible::accSelect method (oleacc.h)

The **IAccessible::accSelect** method modifies the selection or moves the keyboard focus of the specified object. All objects that support selection or receive the keyboard focus must support this method.

## Syntax

```
HRESULT accSelect(
  [in] long    flagsSelect,
  [in] VARIANT varChild
);
```

## Parameters

`[in] flagsSelect`

Type: **long**

Specifies which selection or focus operations are to be performed. This parameter must have a combination of the [SELFLAG Constants](/en-us/windows/desktop/WinAuto/selflag).

`[in] varChild`

Type: **VARIANT**

Specifies the selected object. If the value is CHILDID\_SELF, the object itself is selected; if a child ID, one of the object's child elements is selected. For more information about initializing the [VARIANT structure](/en-us/windows/desktop/WinAuto/variant-structure), see [How Child IDs Are Used in Parameters](/en-us/windows/desktop/WinAuto/how-child-ids-are-used-in-parameters).

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If successful, returns S\_OK.

If not successful, returns one of the values in the table that follows, or another standard [COM error code](/en-us/windows/desktop/WinAuto/return-values).

| Error | Description |
| --- | --- |
| **S\_FALSE** | The specified object is not selected. |
| **E\_INVALIDARG** | An argument is not valid. This return value means that the specified SELFLAG combination is not valid, or that the SELFLAG value does not make sense for the specified object. For example, the following flags are not allowed on a single-selection list box: [SELFLAG\_EXTENDSELECTION](/en-us/windows/desktop/WinAuto/selflag), [SELFLAG\_ADDSELECTION](/en-us/windows/desktop/WinAuto/selflag), and [SELFLAG\_REMOVESELECTION](/en-us/windows/desktop/WinAuto/selflag). |
| **DISP\_E\_MEMBERNOTFOUND** | The object does not support this method. |

## Remarks

Client applications use this method to perform complex selection operations. For more information, see [Selecting Child Objects](/en-us/windows/desktop/WinAuto/selecting-child-objects). This method provides the simplest way to programmatically switch the input focus between applications. This applies to applications running on Windows 2000.

**Note:**This method is for the selection of items, not text.

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

[IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible)

[IAccessible::get\_accFocus](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccessible-get_accfocus)

[IAccessible::get\_accSelection](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccessible-get_accselection)

[SELFLAG](/en-us/windows/desktop/WinAuto/selflag)

[Selection and Focus Properties and Methods](/en-us/windows/desktop/WinAuto/selection-and-focus-properties-and-methods)

[VARIANT](/en-us/windows/desktop/WinAuto/variant-structure)

---
