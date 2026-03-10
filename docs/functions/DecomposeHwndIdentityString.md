# DecomposeHwndIdentityString

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/oleacc/nf-oleacc-iaccpropservices-decomposehwndidentitystring)

# IAccPropServices::DecomposeHwndIdentityString method (oleacc.h)

Use this method to determine the **HWND**, object ID, and child ID for the accessible element identified by the identity string.

## Syntax

```
HRESULT DecomposeHwndIdentityString(
  [in]  const BYTE *pIDString,
  [in]  DWORD      dwIDStringLen,
  [out] HWND       *phwnd,
  [out] DWORD      *pidObject,
  [out] DWORD      *pidChild
);
```

## Parameters

`[in] pIDString`

Type: **const [BYTE](/en-us/windows/desktop/WinProg/windows-data-types)\***

Pointer to a buffer containing identity string of an **HWND**-based accessible element.

`[in] dwIDStringLen`

Type: **[DWORD](/en-us/windows/desktop/WinProg/windows-data-types)**

Specifies the length of the identity string specified by *pIDString*.

`[out] phwnd`

Type: **[HWND](/en-us/windows/desktop/WinProg/windows-data-types)\***

Pointer to a buffer that receives the **HWND** of the accessible element.

`[out] pidObject`

Type: **[DWORD](/en-us/windows/desktop/WinProg/windows-data-types)\***

Pointer to a buffer that receives the object ID of the accessible element.

`[out] pidChild`

Type: **[DWORD](/en-us/windows/desktop/WinProg/windows-data-types)\***

Pointer to a buffer that receives the child ID of the accessible element.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If successful, returns S\_OK.

Returns E\_INVALIDARG if *phwnd*, *pidObject*, or *pidChild* are not valid, or if the given identity string is not a **HWND**-based identity string.

May return other error codes under exceptional error conditions such as low memory.

## Remarks

This method succeeds only if the provided identity string is a **HWND**-based identity string. This method is useful when used in an [IAccPropServer](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccpropserver) callback server that was registered with ANNO\_CONTAINER scope because it allows the server to determine, from the given identity string, the child element (*idChild*) for which the client is calling the server.

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
