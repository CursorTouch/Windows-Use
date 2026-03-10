# ACCESSTIMEOUT

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-accesstimeout)

# ACCESSTIMEOUT structure (winuser.h)

Contains information about the time-out period associated with the Microsoft Win32 accessibility features.

The accessibility time-out period is the length of time that must pass without keyboard and mouse input before the operating system automatically turns off accessibility features. The accessibility time-out is designed for computers that are shared by several users so that options selected by one user do not inconvenience a subsequent user.

The accessibility features affected by the time-out are
the FilterKeys features (SlowKeys, BounceKeys, and
RepeatKeys), MouseKeys, ToggleKeys, and StickyKeys. The
accessibility time-out also affects the high contrast mode
setting.

## Syntax

```
typedef struct tagACCESSTIMEOUT {
  UINT  cbSize;
  DWORD dwFlags;
  DWORD iTimeOutMSec;
} ACCESSTIMEOUT, *LPACCESSTIMEOUT;
```

## Members

`cbSize`

Type: **[UINT](/en-us/windows/desktop/WinProg/windows-data-types)**

Specifies the size, in bytes, of this structure.

`dwFlags`

Type: **[DWORD](/en-us/windows/desktop/WinProg/windows-data-types)**

A set of bit flags that specify properties of the time-out behavior for accessibility features. The following values are defined.

| Value | Meaning |
| --- | --- |
| **ATF\_ONOFFFEEDBACK**  0x00000002 | If this flag is set, the operating system plays a descending siren sound when the time-out period elapses and the accessibility features are turned off. |
| **ATF\_TIMEOUTON**  0x00000001 | If this flag is set, a time-out period has been set for accessibility features. If this flag is not set, the features will not time out even though a time-out period is specified. |

`iTimeOutMSec`

Type: **[DWORD](/en-us/windows/desktop/WinProg/windows-data-types)**

Specifies the time-out period, in milliseconds.

## Remarks

Use an **ACCESSTIMEOUT** structure when calling the [SystemParametersInfo](/en-us/windows/desktop/api/winuser/nf-winuser-systemparametersinfoa) function with the *uiAction* parameter set to the **SPI\_GETACCESSTIMEOUT** or **SPI\_SETACCESSTIMEOUT** value. When using **SPI\_GETACCESSTIMEOUT**, you must specify the **cbSize** member of the **ACCESSTIMEOUT** structure; the **SystemParametersInfo** function fills in the remaining members. Specify all structure members when using the **SPI\_SETACCESSTIMEOUT** value.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 2000 Professional [desktop apps only] |
| **Minimum supported server** | Windows 2000 Server [desktop apps only] |
| **Header** | winuser.h (include Windows.h) |

## See also

[Accessibility Structures](/en-us/windows/desktop/WinAuto/accessibility-structures)

[SystemParametersInfo](/en-us/windows/desktop/api/winuser/nf-winuser-systemparametersinfoa)

---
