# HIGHCONTRASTA

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-highcontrasta)

# HIGHCONTRASTA structure (winuser.h)

Contains information about the high contrast accessibility feature.This feature sets the appearance scheme of the user interface for maximum visibility for a visually-impaired user, and advises applications to comply with this appearance scheme.

## Syntax

```
typedef struct tagHIGHCONTRASTA {
  UINT  cbSize;
  DWORD dwFlags;
  LPSTR lpszDefaultScheme;
} HIGHCONTRASTA, *LPHIGHCONTRASTA;
```

## Members

`cbSize`

Type: **[UINT](/en-us/windows/desktop/WinProg/windows-data-types)**

Specifies the size, in bytes, of this structure.

`dwFlags`

Type: **[DWORD](/en-us/windows/desktop/WinProg/windows-data-types)**

Specifies a combination of the following values:

| Value | Meaning |
| --- | --- |
| **HCF\_HIGHCONTRASTON**  0x00000001 | The high contrast feature is on. |
| **HCF\_AVAILABLE**  0x00000002 | The high contrast feature is available. |
| **HCF\_HOTKEYACTIVE**  0x00000004 | The user can turn the high contrast feature on and off by simultaneously pressing the left ALT, left SHIFT, and PRINT SCREEN keys. |
| **HCF\_CONFIRMHOTKEY**  0x00000008 | A confirmation dialog appears when the high contrast feature is activated by using the hot key. |
| **HCF\_HOTKEYSOUND**  0x00000010 | A siren is played when the user turns the high contrast feature on or off by using the hot key. |
| **HCF\_INDICATOR**  0x00000020 | A visual indicator is displayed when the high contrast feature is on. This value is not currently used and is ignored. |
| **HCF\_HOTKEYAVAILABLE**  0x00000040 | The hot key associated with the high contrast feature can be enabled. An application can retrieve this value, but cannot set it. |
| **HCF\_OPTION\_NOTHEMECHANGE**  0x00001000 | Passing HIGHCONTRASTSTRUCTURE in calls to SystemParametersInfoA can cause theme change effects even if the theme isn't being changed. For example, the WM\_THEMECHANGED message is sent to Windows even if the only change is to HCF\_HOTKEYSOUND.  To prevent this, include the HCF\_OPTION\_NOTHEMECHANGE flag in the call to SystemParametersInfo.  Note  The HCF\_OPTION\_NOTHEMECHANGE flag should not be used when toggling the high contrast mode (HCF\_HIGHCONTRASTON). |

`lpszDefaultScheme`

Type: **[LPTSTR](/en-us/windows/desktop/WinProg/windows-data-types)**

Points to a string that contains the name of the color scheme that will be set to the default scheme.

## Remarks

An application uses this structure when calling the [SystemParametersInfoA function](nf-winuser-systemparametersinfoa) with the **SPI\_GETHIGHCONTRAST** or **SPI\_SETHIGHCONTRAST** value. When using **SPI\_GETHIGHCONTRAST**, an application must specify the **cbSize** member of the **HIGHCONTRAST** structure; the **SystemParametersInfo** function fills the remaining members. An application must specify all structure members when using the **SPI\_SETHIGHCONTRAST** value.

Note

The winuser.h header defines HIGHCONTRAST as an alias that automatically selects the ANSI or Unicode version of this function based on the definition of the UNICODE preprocessor constant. Mixing usage of the encoding-neutral alias with code that is not encoding-neutral can lead to mismatches that result in compilation or runtime errors. For more information, see [Conventions for Function Prototypes](/en-us/windows/win32/intl/conventions-for-function-prototypes).

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 2000 Professional [desktop apps only] |
| **Minimum supported server** | Windows 2000 Server [desktop apps only] |
| **Header** | winuser.h (include Windows.h) |

## See also

[SystemParametersInfoA function](nf-winuser-systemparametersinfoa), [HIGHCONTRASTW structure](ns-winuser-highcontrastw), [Accessibility Structures](/en-us/windows/desktop/WinAuto/accessibility-structures), [SystemParametersInfo](/en-us/windows/desktop/api/winuser/nf-winuser-systemparametersinfoa)

---
