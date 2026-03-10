# ComposeHmenuIdentityString

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/oleacc/nf-oleacc-iaccpropservices-composehmenuidentitystring)

# IAccPropServices::ComposeHmenuIdentityString method (oleacc.h)

Callers use **ComposeHmenuIdentityString**
to retrieve an identity string for an **HMENU**-based accessible element.

## Syntax

```
HRESULT ComposeHmenuIdentityString(
  [in]  HMENU hmenu,
  [in]  DWORD idChild,
  [out] BYTE  **ppIDString,
  [out] DWORD *pdwIDStringLen
);
```

## Parameters

`[in] hmenu`

Type: **[HMENU](/en-us/windows/desktop/WinProg/windows-data-types)**

Identifies the **HMENU**-based accessible element.

`[in] idChild`

Type: **[DWORD](/en-us/windows/desktop/WinProg/windows-data-types)**

Specifies the child ID of the accessible element.

`[out] ppIDString`

Type: **[BYTE](/en-us/windows/desktop/WinProg/windows-data-types)\*\***

Pointer to a buffer that receives the identity string. The callee allocates this buffer using [CoTaskMemAlloc](/en-us/windows/desktop/api/combaseapi/nf-combaseapi-cotaskmemalloc). When finished, the caller must free the buffer by calling [CoTaskMemFree](/en-us/windows/desktop/api/combaseapi/nf-combaseapi-cotaskmemfree).

`[out] pdwIDStringLen`

Type: **[DWORD](/en-us/windows/desktop/WinProg/windows-data-types)\***

Pointer to a buffer that receives the length of the identity string.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If successful, returns S\_OK.

Returns E\_INVALIDARG if *hmenu* or *idChild* is not valid.

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

---
