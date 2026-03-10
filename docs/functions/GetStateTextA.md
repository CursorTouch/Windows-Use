# GetStateTextA

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/oleacc/nf-oleacc-getstatetexta)

# GetStateTextA function (oleacc.h)

Retrieves a localized string that describes an object's state for a single predefined state bit flag. Because state values are a combination of one or more bit flags, clients call this function more than once to retrieve all state strings.

## Syntax

```
UINT GetStateTextA(
  [in]  DWORD lStateBit,
  [out] LPSTR lpszState,
  [in]  UINT  cchState
);
```

## Parameters

`[in] lStateBit`

Type: **[DWORD](/en-us/windows/desktop/WinProg/windows-data-types)**

One of the [object state constants](/en-us/windows/desktop/WinAuto/object-state-constants).

`[out] lpszState`

Type: **[LPTSTR](/en-us/windows/desktop/WinProg/windows-data-types)**

Address of a buffer that receives the state text string. If this parameter is **NULL**, the function returns the state string's length, not including the null character.

`[in] cchState`

Type: **[UINT](/en-us/windows/desktop/WinProg/windows-data-types)**

The size of the buffer that is pointed to by the *lpszStateBit* parameter. For ANSI strings, this value is measured in bytes; for Unicode strings, it is measured in characters.

## Return value

Type: **[UINT](/en-us/windows/desktop/WinProg/windows-data-types)**

If successful, and if *lpszStateBit* is non-**NULL**, the return value is the number of bytes (ANSI strings) or characters (Unicode strings) that are copied into the buffer, not including the null-terminated character. If *lpszStateBit* is **NULL**, the return value represents the string's length, not including the null character.

If the string resource does not exist, or if the *lpszStateBit* parameter is not a valid pointer, the return value is zero (0). To get extended error information, call [GetLastError](/en-us/windows/desktop/api/errhandlingapi/nf-errhandlingapi-getlasterror).

## Remarks

This function accepts only one state bit at a time, not a bitmask.

Note

The oleacc.h header defines GetStateText as an alias that automatically selects the ANSI or Unicode version of this function based on the definition of the UNICODE preprocessor constant. Mixing usage of the encoding-neutral alias with code that is not encoding-neutral can lead to mismatches that result in compilation or runtime errors. For more information, see [Conventions for Function Prototypes](/en-us/windows/win32/intl/conventions-for-function-prototypes).

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
