# GetImplementationID

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/msaatext/nf-msaatext-iversioninfo-getimplementationid)

# IVersionInfo::GetImplementationID method (msaatext.h)

Clients call **IVersionInfo::GetImplementationID** to retrieve a unique identifier for the component.

**Note**  Active Accessibility Text Services is deprecated. Please see
[Microsoft Windows Text Services Framework](/en-us/windows/win32/tsf/text-services-framework) for more information on advanced text input and natural language technologies.

## Syntax

```
HRESULT GetImplementationID(
  [in]  ULONG ulSub,
  [out] GUID  *implid
);
```

## Parameters

`[in] ulSub`

Type: **[ULONG](/en-us/windows/desktop/WinProg/windows-data-types)**

The ordinal position of the component in the tree.

`[out] implid`

Type: **GUID\***

An implementation identifier for the component. The implementation identifier is unique for this component and is used only for comparing components.

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
