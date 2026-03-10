# GetIdentityString

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/oleacc/nf-oleacc-iaccidentity-getidentitystring)

# IAccIdentity::GetIdentityString method (oleacc.h)

Retrieves a string of bytes (an identity string) that uniquely identifies an accessible element.

If server developers know the **HWND** of the object they want to annotate, they can use one of the following methods instead of using this
method and getting an identity string.

* [IAccPropServices::SetHwndPropStr](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccpropservices-sethwndpropstr)
* [IAccPropServices::SetHwndProp](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccpropservices-sethwndprop)
* [IAccPropServices::SetHwndPropServer](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccpropservices-sethwndpropserver)

## Syntax

```
HRESULT GetIdentityString(
  [in]  DWORD dwIDChild,
  [out] BYTE  **ppIDString,
  [out] DWORD *pdwIDStringLen
);
```

## Parameters

`[in] dwIDChild`

Type: **[DWORD](/en-us/windows/desktop/WinProg/windows-data-types)**

Specifies which child of the [IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible) object the caller wants to identify.

`[out] ppIDString`

Type: **[BYTE](/en-us/windows/desktop/WinProg/windows-data-types)\*\***

Address of a variable that receives a pointer to a callee-allocated identity string. The callee allocates the identity string using [CoTaskMemAlloc](/en-us/windows/desktop/api/combaseapi/nf-combaseapi-cotaskmemalloc); the caller must release the identity string by using [CoTaskMemFree](/en-us/windows/desktop/api/combaseapi/nf-combaseapi-cotaskmemfree) when finished.

`[out] pdwIDStringLen`

Type: **[DWORD](/en-us/windows/desktop/WinProg/windows-data-types)\***

Address of a variable that receives the length, in bytes, of the callee-allocated identity string.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

Return S\_OK, except under exceptional error conditions, such as low memory. If not supported, calling [QueryInterface](/en-us/windows/desktop/api/unknwn/nf-unknwn-iunknown-queryinterface(q)) on [IAccIdentity](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccidentity) should fail.

## Remarks

The returned string should be considered opaque; clients should use it only as a whole, and should not attempt to dissect it or otherwise interpret it manually.

If a client knows or expects that a string is HWNDâbased, it can use [IAccPropServices::DecomposeHwndIdentityString](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccpropservices-decomposehwndidentitystring) to attempt to decompose the identity string.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows Vista or Windows XP |
| **Minimum supported server** | Windows Server 2003 |
| **Target Platform** | Windows |
| **Header** | oleacc.h (include OleAcc.h Include Initguid.h first.) |
| **DLL** | Oleacc.dll |
| **Redistributable** | Active Accessibility 2.0 RDK on Windows NT 4.0 with SP6 and later and Windows 98 |

---
