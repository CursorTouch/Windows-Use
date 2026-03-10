# SetPropValue

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/oleacc/nf-oleacc-iaccpropservices-setpropvalue)

# IAccPropServices::SetPropValue method (oleacc.h)

Use **SetPropValue** to identify the accessible element to be annotated, specify the property to be annotated, and provide a new value for that property.

If server developers know the **HWND** of the accessible element they want to annotate, they can use one of the following methods:

* [IAccPropServices::SetHwndPropStr](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccpropservices-sethwndpropstr),
* [IAccPropServices::SetHwndProp](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccpropservices-sethwndprop), or
* [IAccPropServices::SetHwndPropServer](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccpropservices-sethwndpropserver)

## Syntax

```
HRESULT SetPropValue(
  [in] const BYTE *pIDString,
  [in] DWORD      dwIDStringLen,
  [in] MSAAPROPID idProp,
  [in] VARIANT    var
);
```

## Parameters

`[in] pIDString`

Type: **const [BYTE](/en-us/windows/desktop/WinProg/windows-data-types)\***

Identifies the accessible element that is to be annotated.

`[in] dwIDStringLen`

Type: **[DWORD](/en-us/windows/desktop/WinProg/windows-data-types)**

Specifies the length of the string identified by the *pIDString* parameter.

`[in] idProp`

Type: **MSAAPROPID**

Specifies the property of the accessible element to be annotated.

`[in] var`

Type: **VARIANT**

Specifies a new value for the property.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If successful, returns S\_OK.

Returns E\_INVALIDARG if *idProp* is not a supported property, if *var* is not a supported type for that property, or if the identity string is not valid.

May return other error codes under exceptional error conditions such as low memory.

## Remarks

See the support section for a list of supported properties and their expected types. Note that currently some properties are supported only when a callback is used and cannot be specified directly using this method.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps only] |
| **Minimum supported server** | Windows Server 2003 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | oleacc.h (include OleAcc.h Include Initguid.h first.) |
| **DLL** | Oleacc.dll |
| **Redistributable** | Active Accessibility 2.0 RDK on Windows NT 4.0 with SP6 and later and Windows 98 |

---
