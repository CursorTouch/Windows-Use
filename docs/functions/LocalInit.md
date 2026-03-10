# LocalInit

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/msaatext/nf-msaatext-icocreatedlocally-localinit)

# ICoCreatedLocally::LocalInit method (msaatext.h)

Implemented by clients to return information about the local object.

**Note**  Active Accessibility Text Services is deprecated. Please see  
[Microsoft Windows Text Services Framework](/en-us/windows/win32/tsf/text-services-framework) for more information on advanced text input and natural language technologies.

## Syntax

```
HRESULT LocalInit(
  [in] IUnknown *punkLocalObject,
  [in] REFIID   riidParam,
  [in] IUnknown *punkParam,
  [in] VARIANT  varParam
);
```

## Parameters

`[in] punkLocalObject`

Type: **IUnknown\***

A pointer to the server object.

`[in] riidParam`

Type: **REFIID**

An optional interface parameter that is passed to the new helper object. This parameter specifies an interface identifier.

`[in] punkParam`

Type: **IUnknown\***

An optional interface parameter that is passed to the new helper object. This parameter specifies the interface pointer.

`[in] varParam`

Type: **VARIANT**

An optional interface parameter that is passed to the new helper object.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If successful, returns S\_OK. If not successful, returns a standard [COM error code](/en-us/windows/desktop/WinAuto/return-values).

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps only] |
| **Minimum supported server** | Windows Server 2003 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | msaatext.h |
| **DLL** | Msaatext.dll |
| **Redistributable** | Active Accessibility 2.0 RDK on Windows NT 4.0 with SP6 and later and Windows 98 |

---
