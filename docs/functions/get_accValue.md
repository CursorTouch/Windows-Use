# get_accValue

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/oleacc/nf-oleacc-iaccessible-get_accvalue)

# IAccessible::get\_accValue method (oleacc.h)

The **IAccessible::get\_accValue** method retrieves the value of the specified object. Not all objects have a value.

## Syntax

```
HRESULT get_accValue(
  [in]          VARIANT varChild,
  [out, retval] BSTR    *pszValue
);
```

## Parameters

`[in] varChild`

Type: **VARIANT**

Specifies whether the retrieved value information belongs to the object or one of the object's child elements. This parameter is either CHILDID\_SELF (to obtain information about the object) or a child ID (to obtain information about the object's child element). For more information about initializing the [VARIANT structure](/en-us/windows/desktop/WinAuto/variant-structure), see [How Child IDs Are Used in Parameters](/en-us/windows/desktop/WinAuto/how-child-ids-are-used-in-parameters).

`[out, retval] pszValue`

Type: **BSTR\***

Address of the **BSTR** that receives a localized string that contains the object's current value.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If successful, returns S\_OK.

If not successful, returns one of the values in the table that follows, or another standard [COM error code](/en-us/windows/desktop/WinAuto/return-values). Servers return these values, but clients must always check output parameters to ensure that they contain valid values. For more information, see [Checking IAccessible Return Values](/en-us/windows/desktop/WinAuto/checking-iaccessible-return-values).

| Error | Description |
| --- | --- |
| **DISP\_E\_MEMBERNOTFOUND** | The object does not support this property. |
| **E\_INVALIDARG** | An argument is not valid. |

## Remarks

Numeric values returned from scroll bar and trackbar accessible objects indicate percentages. They are integers between zero (0) and one hundred (100), inclusive, but might also be a limited range for example, between one (1) and sixteen (16). Also, some scroll bar and trackbar objects return strings that correspond to settings such as screen size or Internet security.

**Note to server developers:**Localize the string returned from this property.

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

[Value Property](/en-us/windows/desktop/WinAuto/value-property)

---
