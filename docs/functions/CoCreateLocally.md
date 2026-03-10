# CoCreateLocally

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/msaatext/nf-msaatext-icocreatelocally-cocreatelocally)

# ICoCreateLocally::CoCreateLocally method (msaatext.h)

Clients call **ICoCreateLocally::CoCreateLocally** to create a helper object in the same context as the server object. This allows clients to increase performance because they are running in the server application.

**Note**  Active Accessibility Text Services is deprecated. Please see  
[Microsoft Windows Text Services Framework](/en-us/windows/win32/tsf/text-services-framework) for more information on advanced text input and natural language technologies.

## Syntax

```
HRESULT CoCreateLocally(
  [in]  REFCLSID rclsid,
  [in]  DWORD    dwClsContext,
  [in]  REFIID   riid,
  [out] IUnknown **punk,
  [in]  REFIID   riidParam,
  [in]  IUnknown *punkParam,
  [in]  VARIANT  varParam
);
```

## Parameters

`[in] rclsid`

Type: **REFCLSID**

Class identifier of the object to be created locally.

`[in] dwClsContext`

Type: **[DWORD](/en-us/windows/desktop/WinProg/windows-data-types)**

Context in which the helper object should run. This is usually CLSCTX\_INPROC\_SERVER.

`[in] riid`

Type: **REFIID**

The desired interface identifier (IID).

`[out] punk`

Type: **IUnknown\***

Interface pointer to the desired interface identifier (from *riid*).

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

If successful, returns S\_OK.

If not successful, returns the following value or another standard COM error code.

| Error | Description |
| --- | --- |
| **E\_ACCESSDENIED** | The client does not have sufficient permissions to create this object in the server process. |

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
