# put_accValue

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/oleacc/nf-oleacc-iaccessible-put_accvalue)

# IAccessible::put\_accValue method (oleacc.h)

The **IAccessible::put\_accValue** method sets the value of the specified object. Not all objects have a value.

## Syntax

```
HRESULT put_accValue(
  [in] VARIANT varChild,
  [in] BSTR    szValue
);
```

## Parameters

`[in] varChild`

Type: **VARIANT**

Specifies whether the value information being set belongs to the object or one of the object's child elements. This parameter is either CHILDID\_SELF (to set information on the object) or a child ID (to set information about the object's child element). For more information about initializing the [VARIANT structure](/en-us/windows/desktop/WinAuto/variant-structure), see [How Child IDs Are Used in Parameters](/en-us/windows/desktop/WinAuto/how-child-ids-are-used-in-parameters).

`[in] szValue`

Type: **BSTR**

A localized string that contains the object's value.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If successful, returns S\_OK.

If not successful, returns one of the values in the table that follows, or another standard [COM error code](/en-us/windows/desktop/WinAuto/return-values). Servers return these values, but clients must always check output parameters to ensure that they contain valid values. For more information, see [Checking IAccessible Return Values](/en-us/windows/desktop/WinAuto/checking-iaccessible-return-values).

| Error | Description |
| --- | --- |
| **DISP\_E\_MEMBERNOTFOUND** | The object does not support this property. |
| **E\_INVALIDARG** | An argument is not valid. |

## Remarks

The **IAccessible::put\_accValue** method is supported for some UI elements (usually edit controls). For UI elements that do not support this method, control-specific methods are used instead. For more information, see [Supported User Interface Element Reference](/en-us/windows/desktop/WinAuto/appendix-a--supported-user-interface-elements-reference).

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

---
