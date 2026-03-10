# DecomposeHmenuIdentityString

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/oleacc/nf-oleacc-iaccpropservices-decomposehmenuidentitystring)

# IAccPropServices::DecomposeHmenuIdentityString method (oleacc.h)

Use this method to determine the **HMENU**, object ID, and child ID for the accessible element identified by the identity string.

## Syntax

```
HRESULT DecomposeHmenuIdentityString(
  [in]  const BYTE *pIDString,
  [in]  DWORD      dwIDStringLen,
  [out] HMENU      *phmenu,
  [out] DWORD      *pidChild
);
```

## Parameters

`[in] pIDString`

Type: **const [BYTE](/en-us/windows/desktop/WinProg/windows-data-types)\***

Pointer to a buffer containing identity string of an **HMENU**-based accessible element.

`[in] dwIDStringLen`

Type: **[DWORD](/en-us/windows/desktop/WinProg/windows-data-types)**

Specifies the length of the identity string specified by *pIDString*.

`[out] phmenu`

Type: **[HMENU](/en-us/windows/desktop/WinProg/windows-data-types)\***

Pointer to a buffer that receives the **HMENU** of the accessible element.

`[out] pidChild`

Type: **[DWORD](/en-us/windows/desktop/WinProg/windows-data-types)\***

Pointer to a buffer that receives the child ID of the accessible element.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If successful, returns S\_OK.

Returns E\_INVALIDARG if *phmenu* or *pidChild* are not valid, or if the given identity string is not a **HMENU**-based identity string.

May return other error codes under exceptional error conditions such as low memory.

## Remarks

This method succeeds only if the provided identity string is an **HMENU**-based identity string. This method is useful in an [IAccPropServer](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccpropserver) callback server that was registered with ANNO\_CONTAINER scope because it allows the server to determine, from the given identity string, the child element (*idChild*) for which the client is calling the server.

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
