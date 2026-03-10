# SetPropServer

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/oleacc/nf-oleacc-iaccpropservices-setpropserver)

# IAccPropServices::SetPropServer method (oleacc.h)

Servers use **SetPropServer** to specify a callback object to be used to annotate an array of properties for the accessible element. You can also specify whether the annotation is to be applied to this accessible element or to the element and its children. This method is used for [server annotation](/en-us/windows/desktop/WinAuto/server-annotation).

If server developers know the **HWND** of the accessible element they want to annotate, they can use [IAccPropServices::SetHwndPropServer](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccpropservices-sethwndpropserver).

## Syntax

```
HRESULT SetPropServer(
  [in] const BYTE       *pIDString,
  [in] DWORD            dwIDStringLen,
  [in] const MSAAPROPID *paProps,
  [in] int              cProps,
  [in] IAccPropServer   *pServer,
  [in] AnnoScope        annoScope
);
```

## Parameters

`[in] pIDString`

Type: **const [BYTE](/en-us/windows/desktop/WinProg/windows-data-types)\***

Identifies the accessible element that is to be annotated.

`[in] dwIDStringLen`

Type: **[DWORD](/en-us/windows/desktop/WinProg/windows-data-types)**

Specifies the length of the string identified by the *pIDString* parameter.

`[in] paProps`

Type: **const MSAAPROPID\***

Specifies an array of properties to be handled by the specified callback object.

`[in] cProps`

Type: **int**

Specifies an array of properties to be handled by the specified callback object.

`[in] pServer`

Type: **IAccPropServer\***

Specifies the callback object that will be invoked when a client requests one of the overridden properties.

`[in] annoScope`

Type: **AnnoScope**

May be ANNO\_THIS, indicating that the annotation affects the indicated accessible element only; or ANNO\_CONTAINER, indicating that it applies to the element and its immediate element children.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If successful, returns S\_OK.

Returns E\_INVALIDARG if any of the properties in the *paProps* array are not supported properties, if the identity string is not valid, or if *annoScope* is not one of ANNO\_THIS or ANNO\_CONTAINER.

May return other error codes under exceptional error conditions such as low memory.

## Remarks

See the support section for a list of supported properties and their expected types.

The annotation run time will use [AddRef](/en-us/windows/desktop/api/unknwn/nf-unknwn-iunknown-addref) to increment the reference counter for the *pServer* callback object appropriately. The caller is free to [Release](/en-us/windows/desktop/api/unknwn/nf-unknwn-iunknown-release) it after calling this method. The annotation run time will automatically release the callback object after the accessible element being annotated is no longer being used.

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
