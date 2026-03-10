# SetHmenuProp

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/oleacc/nf-oleacc-iaccpropservices-sethmenuprop)

# IAccPropServices::SetHmenuProp method (oleacc.h)

This method wraps [SetPropValue](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccpropservices-setpropvalue), providing a convenient entry point for callers who are annotating **HMENU**-based accessible elements. If the new value is a string, you can use [IAccPropServices::SetHmenuPropStr](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccpropservices-sethmenupropstr) instead.

## Syntax

```
HRESULT SetHmenuProp(
  [in] HMENU      hmenu,
  [in] DWORD      idChild,
  [in] MSAAPROPID idProp,
  [in] VARIANT    var
);
```

## Parameters

`[in] hmenu`

Type: **[HMENU](/en-us/windows/desktop/WinProg/windows-data-types)**

Identifies the **HMENU**-based accessible element to be annotated.

`[in] idChild`

Type: **[DWORD](/en-us/windows/desktop/WinProg/windows-data-types)**

Specifies the child ID of the accessible element.

`[in] idProp`

Type: **MSAAPROPID**

Specifies which property of the accessible element is to be annotated.

`[in] var`

Type: **VARIANT**

Specifies a new value for the *idProp* property.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If successful, returns S\_OK.

May return other error codes under exceptional error conditions such as low memory.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps only] |
| **Minimum supported server** | Windows Server 2003 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | oleacc.h (include OleAcc.h Include Initguid.h first.) |
| **DLL** | Oleacc.dll |
| **Redistributable** | Active Accessibility 2.0 RDK on Windows NT 4.0 with SP6 and later and Windows 98 |

## See also

[ClearHmenuProps](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccpropservices-clearhmenuprops)

[IAccPropServices](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccpropservices)

[SetHmenuPropServer](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccpropservices-sethmenupropserver)

[SetHmenuPropStr](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccpropservices-sethmenupropstr)

[SetPropValue](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccpropservices-setpropvalue)

---
