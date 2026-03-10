# GetOleaccVersionInfo

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/oleacc/nf-oleacc-getoleaccversioninfo)

# GetOleaccVersionInfo function (oleacc.h)

Retrieves the version number and build number of the Microsoft Active Accessibility file Oleacc.dll.

## Syntax

```
VOID GetOleaccVersionInfo(
  [out] DWORD *pVer,
  [out] DWORD *pBuild
);
```

## Parameters

`[out] pVer`

Type: **[DWORD](/en-us/windows/desktop/WinProg/windows-data-types)\***

Address of a **DWORD** that receives the version number. The major version number is placed in the high word, and the minor version number is placed in the low word.

`[out] pBuild`

Type: **[DWORD](/en-us/windows/desktop/WinProg/windows-data-types)\***

Address of a **DWORD** that receives the build number. The major build number is placed in the high word, and the minor build number is placed in the low word.

## Return value

None

## Remarks

This function provides an easy way to get the version and build numbers for Oleacc.dll. The [GetFileVersionInfoSize](/en-us/windows/win32/api/winver/nf-winver-getfileversioninfosizea), [GetFileVersionInfo](/en-us/windows/win32/api/winver/nf-winver-getfileversioninfoa), and [VerQueryValue](/en-us/windows/win32/api/winver/nf-winver-verqueryvaluea) functions can be used to retrieve the same information.

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

---
