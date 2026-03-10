# LresultFromObject

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/oleacc/nf-oleacc-lresultfromobject)

# LresultFromObject function (oleacc.h)

Returns a reference, similar to a handle, to the specified object. Servers return this reference when handling [WM\_GETOBJECT](/en-us/windows/desktop/WinAuto/wm-getobject).

## Syntax

```
LRESULT LresultFromObject(
  [in] REFIID    riid,
  [in] WPARAM    wParam,
  [in] LPUNKNOWN punk
);
```

## Parameters

`[in] riid`

Type: **REFIID**

Reference identifier of the interface provided to the client. This parameter is IID\_IAccessible.

`[in] wParam`

Type: **[WPARAM](/en-us/windows/desktop/WinProg/windows-data-types)**

Value sent by the associated [WM\_GETOBJECT](/en-us/windows/win32/winauto/wm-getobject) message in its *wParam* parameter.

`[in] punk`

Type: **LPUNKNOWN**

Address of the [IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible) interface to the object that corresponds to the [WM\_GETOBJECT](/en-us/windows/win32/winauto/wm-getobject) message.

## Return value

Type: **[LRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If successful, returns a positive value that is a reference to the object.

If not successful, returns one of the values in the table that follows, or another standard [COM error code](/en-us/windows/desktop/WinAuto/return-values).

| Return code | Description |
| --- | --- |
| **E\_INVALIDARG** | One or more arguments are not valid. |
| **E\_NOINTERFACE** | The object specified in the *pAcc* parameter does not support the interface specified in the *riid* parameter. |
| **E\_OUTOFMEMORY** | Insufficient memory to store the object reference. |
| **E\_UNEXPECTED** | An unexpected error occurred. |

## Remarks

Servers call this function only when handling the [WM\_GETOBJECT](/en-us/windows/win32/winauto/wm-getobject) message. For an overview of how **LresultFromObject** is related to **WM\_GETOBJECT**, see [How WM\_GETOBJECT Works](/en-us/windows/desktop/WinAuto/how-wm-getobject-works).

**LresultFromObject** increments the object's reference count. If you are not storing the interface pointer passed to the function (that is, you create a new interface pointer for the object each time [WM\_GETOBJECT](/en-us/windows/win32/winauto/wm-getobject) is received), call the object's [Release](/en-us/windows/desktop/api/unknwn/nf-unknwn-iunknown-release) method to decrement the reference count back to one. Then the client calls **Release** and the object is destroyed. For more information, see [How to Handle WM\_GETOBJECT](/en-us/windows/desktop/WinAuto/how-to-handle-wm-getobject).

Each time a server processes [WM\_GETOBJECT](/en-us/windows/win32/winauto/wm-getobject) for a specific object, it calls **LresultFromObject** to obtain a new reference to the object. Servers do not save the reference returned from **LresultFromObject** from one instance of processing **WM\_GETOBJECT** to use as the message's return value when processing subsequent **WM\_GETOBJECT** messages for the same object. This causes the client to receive an error.

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

[Creating Proxy Objects](/en-us/windows/desktop/WinAuto/creating-proxy-objects)

[How WM\_GETOBJECT Works](/en-us/windows/desktop/WinAuto/how-wm-getobject-works)

[How to Handle WM\_GETOBJECT](/en-us/windows/desktop/WinAuto/how-to-handle-wm-getobject)

[WM\_GETOBJECT](/en-us/windows/win32/winauto/wm-getobject)

---
