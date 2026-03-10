# GetBuildVersion

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/msaatext/nf-msaatext-iversioninfo-getbuildversion)

# IVersionInfo::GetBuildVersion method (msaatext.h)

Clients call **IVersionInfo::GetBuildVersion** to retrieve build information for a specified component.

**Note**  Active Accessibility Text Services is deprecated. Please see
[Microsoft Windows Text Services Framework](/en-us/windows/win32/tsf/text-services-framework) for more information on advanced text input and natural language technologies.

## Syntax

```
HRESULT GetBuildVersion(
  [in]  ULONG ulSub,
  [out] DWORD *pdwMajor,
  [out] DWORD *pdwMinor
);
```

## Parameters

`[in] ulSub`

Type: **[ULONG](/en-us/windows/desktop/WinProg/windows-data-types)**

The ordinal position of the component in the tree.

`[out] pdwMajor`

Type: **[DWORD](/en-us/windows/desktop/WinProg/windows-data-types)\***

The major build version of the component specified in *ulSub*.

`[out] pdwMinor`

Type: **[DWORD](/en-us/windows/desktop/WinProg/windows-data-types)\***

The minor build version of the component specified in *ulSub*.

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
