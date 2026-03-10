# SetHwndPropStr

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/oleacc/nf-oleacc-iaccpropservices-sethwndpropstr)

# IAccPropServices::SetHwndPropStr method (oleacc.h)

This method wraps [SetPropValue](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccpropservices-setpropvalue), providing a more convenient entry point for callers who are annotating **HWND**-based accessible elements.

## Syntax

```
HRESULT SetHwndPropStr(
  [in] HWND       hwnd,
  [in] DWORD      idObject,
  [in] DWORD      idChild,
  [in] MSAAPROPID idProp,
  [in] LPCWSTR    str
);
```

## Parameters

`[in] hwnd`

Type: **[HWND](/en-us/windows/desktop/WinProg/windows-data-types)**

Identifies the accessible element that is to be annotated. This replaces the identity string.

`[in] idObject`

Type: **[DWORD](/en-us/windows/desktop/WinProg/windows-data-types)**

Identifies the accessible element that is to be annotated. This replaces the identity string.

`[in] idChild`

Type: **[DWORD](/en-us/windows/desktop/WinProg/windows-data-types)**

Identifies the accessible element that is to be annotated. This replaces the identity string.

`[in] idProp`

Type: **MSAAPROPID**

Specifies which property of that element is to be annotated.

`[in] str`

Type: **[LPCWSTR](/en-us/windows/desktop/WinProg/windows-data-types)**

Specifies a new value for that property.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If successful, returns S\_OK.

May return other error codes under exceptional error conditions such as low memory.

## Remarks

By using this method, the caller does not have to obtain an identity string; it can specify the *hwnd*, *idObject*, and *idChild* parameters directly.

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

[ClearHwndProps](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccpropservices-clearhwndprops)

[IAccPropServices](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccpropservices)

[SetHwndProp](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccpropservices-sethwndprop)

[SetHwndPropServer](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccpropservices-sethwndpropserver)

[SetPropValue](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccpropservices-setpropvalue)

---
