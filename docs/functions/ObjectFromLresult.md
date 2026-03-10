# ObjectFromLresult

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/oleacc/nf-oleacc-objectfromlresult)

# ObjectFromLresult function (oleacc.h)

Retrieves a requested interface pointer for an accessible object based on a previously generated object reference.

This function is designed for internal use by Microsoft Active Accessibility and is documented for informational purposes only. Neither clients nor servers should call this function.

## Syntax

```
HRESULT ObjectFromLresult(
  [in]  LRESULT lResult,
  [in]  REFIID  riid,
  [in]  WPARAM  wParam,
  [out] void    **ppvObject
);
```

## Parameters

`[in] lResult`

Type: **[LRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

A 32-bit value returned by a previous successful call to the [LresultFromObject](/en-us/windows/desktop/api/oleacc/nf-oleacc-lresultfromobject) function.

`[in] riid`

Type: **REFIID**

Reference identifier of the interface to be retrieved. This is IID\_IAccessible.

`[in] wParam`

Type: **[WPARAM](/en-us/windows/desktop/WinProg/windows-data-types)**

Value sent by the associated [WM\_GETOBJECT](/en-us/windows/win32/winauto/wm-getobject) message in its *wParam* parameter.

`[out] ppvObject`

Type: **void\*\***

Receives the address of the [IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible) interface on the object that corresponds to the [WM\_GETOBJECT](/en-us/windows/win32/winauto/wm-getobject) message.

## Return value

Type: **STDAPI**

If successful, returns S\_OK.

If not successful, returns one of the following standard [COM error codes](/en-us/windows/desktop/WinAuto/return-values).

| Return code | Description |
| --- | --- |
| **E\_INVALIDARG** | One or more arguments are not valid. This occurs when the *lResult* parameter specified is not a value obtained by a call to [LresultFromObject](/en-us/windows/desktop/api/oleacc/nf-oleacc-lresultfromobject), or when *lResult* is a value used on a previous call to [ObjectFromLresult](/en-us/windows/desktop/api/oleacc/nf-oleacc-objectfromlresult). |
| **E\_NOINTERFACE** | The object specified in the *ppvObject* parameter does not support the interface specified by the *riid* parameter. |
| **E\_OUTOFMEMORY** | Insufficient memory to store the object reference. |
| **E\_UNEXPECTED** | An unexpected error occurred. |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps only] |
| **Minimum supported server** | Windows Server 2003 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | oleacc.h |
| **Library** | Oleacc.lib |
| **DLL** | Oleacc.dll |
| **Redistributable** | Active Accessibility 2.0 RDK on Windows NT 4.0 with SP6 and later and Windows 98 |

## See also

[WM\_GETOBJECT](/en-us/windows/win32/winauto/wm-getobject)

---
