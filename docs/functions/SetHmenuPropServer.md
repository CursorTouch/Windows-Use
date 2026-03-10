# SetHmenuPropServer

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/oleacc/nf-oleacc-iaccpropservices-sethmenupropserver)

# IAccPropServices::SetHmenuPropServer method (oleacc.h)

This method wraps [SetPropServer](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccpropservices-setpropserver), providing a convenient entry point for callers who are annotating **HMENU**-based accessible elements.

## Syntax

```
HRESULT SetHmenuPropServer(
  [in] HMENU            hmenu,
  [in] DWORD            idChild,
  [in] const MSAAPROPID *paProps,
  [in] int              cProps,
  [in] IAccPropServer   *pServer,
  [in] AnnoScope        annoScope
);
```

## Parameters

`[in] hmenu`

Type: **[HMENU](/en-us/windows/desktop/WinProg/windows-data-types)**

Identifies the **HMENU**-accessible element to be annotated.

`[in] idChild`

Type: **[DWORD](/en-us/windows/desktop/WinProg/windows-data-types)**

Identifies the accessible element that is to be annotated. This replaces the identity string.

`[in] paProps`

Type: **const MSAAPROPID\***

Specifies an array of properties that is to be handled by the specified callback object.

`[in] cProps`

Type: **int**

Specifies the number of properties in the *paProps* array.

`[in] pServer`

Type: **IAccPropServer\***

Specifies the callback object, which will be invoked when a client requests one of the overridden properties.

`[in] annoScope`

Type: **AnnoScope**

May be ANNO\_THIS, indicating that the annotation affects the indicated accessible element only; or ANNO\_CONTAINER, indicating that it applies to the element and its immediate element children.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If successful, returns S\_OK.

Returns E\_INVALIDARG if any of the properties in the *paProps* array are not supported properties, if the identity string is not valid, or if *annoScope* is not one of ANNO\_THIS or ANNO\_CONTAINER.

May return other error codes under exceptional error conditions such as low memory.

## Remarks

By using this method, the caller does not have to obtain an identity string; it can specify the *hmenu* and *idChild* parameters directly.

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

[SetHmenuProp](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccpropservices-sethmenuprop)

[SetHmenuPropStr](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccpropservices-sethmenupropstr)

[SetPropServer](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccpropservices-setpropserver)

---
