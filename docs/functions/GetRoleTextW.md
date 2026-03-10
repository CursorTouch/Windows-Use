# GetRoleTextW

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/oleacc/nf-oleacc-getroletextw)

# GetRoleTextW function (oleacc.h)

Retrieves the localized string that describes the object's role for the specified role value.

## Syntax

```
UINT GetRoleTextW(
  [in]  DWORD  lRole,
  [out] LPWSTR lpszRole,
  [in]  UINT   cchRoleMax
);
```

## Parameters

`[in] lRole`

Type: **[DWORD](/en-us/windows/desktop/WinProg/windows-data-types)**

One of the [object role](/en-us/windows/desktop/WinAuto/object-roles) constants.

`[out] lpszRole`

Type: **[LPTSTR](/en-us/windows/desktop/WinProg/windows-data-types)**

Address of a buffer that receives the role text string. If this parameter is **NULL**, the function returns the role string's length, not including the null character.

`[in] cchRoleMax`

Type: **[UINT](/en-us/windows/desktop/WinProg/windows-data-types)**

The size of the buffer that is pointed to by the *lpszRole* parameter. For ANSI strings, this value is measured in bytes; for Unicode strings, it is measured in characters.

## Return value

Type: **[UINT](/en-us/windows/desktop/WinProg/windows-data-types)**

If successful, and if *lpszRole* is non-**NULL**, the return value is the number of bytes (ANSI strings) or characters (Unicode strings) copied into the buffer, not including the terminating null character. If *lpszRole* is **NULL**, the return value represents the string's length, not including the null character.

If the string resource does not exist, or if the *lpszRole* parameter is not a valid pointer, the return value is zero (0). To get extended error information, call [GetLastError](/en-us/windows/desktop/api/errhandlingapi/nf-errhandlingapi-getlasterror).

## Remarks

Note

The oleacc.h header defines GetRoleText as an alias that automatically selects the ANSI or Unicode version of this function based on the definition of the UNICODE preprocessor constant. Mixing usage of the encoding-neutral alias with code that is not encoding-neutral can lead to mismatches that result in compilation or runtime errors. For more information, see [Conventions for Function Prototypes](/en-us/windows/win32/intl/conventions-for-function-prototypes).

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
