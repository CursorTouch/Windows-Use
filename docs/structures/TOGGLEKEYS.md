# TOGGLEKEYS

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-togglekeys)

# TOGGLEKEYS structure (winuser.h)

Contains information about the ToggleKeys accessibility feature. When the ToggleKeys feature is on, the computer emits a high-pitched tone whenever the user turns on the CAPS LOCK, NUM LOCK, or SCROLL LOCK key, and a low-pitched tone whenever the user turns off one of those keys.

## Syntax

```
typedef struct tagTOGGLEKEYS {
  UINT  cbSize;
  DWORD dwFlags;
} TOGGLEKEYS, *LPTOGGLEKEYS;
```

## Members

`cbSize`

Type: **[DWORD](/en-us/windows/desktop/WinProg/windows-data-types)**

Specifies the size, in bytes, of this structure.

`dwFlags`

Type: **[DWORD](/en-us/windows/desktop/WinProg/windows-data-types)**

A set of bit flags that specify properties of the ToggleKeys feature. The following bit flag values are defined:

| Value | Meaning |
| --- | --- |
| **TKF\_AVAILABLE**  0x00000002 | If this flag is set, the ToggleKeys feature is available. |
| **TKF\_CONFIRMHOTKEY**  0x00000008 | **Windows 95/98, Windows 2000:** A confirmation dialog box appears when the ToggleKeys feature is activated by using the hot key. |
| **TKF\_HOTKEYACTIVE**  0x00000004 | If this flag is set, the user can turn the ToggleKeys feature on and off by holding down the NUM LOCK key for eight seconds. |
| **TKF\_HOTKEYSOUND**  0x00000010 | If this flag is set, the system plays a siren sound when the user turns the ToggleKeys feature on or off by using the hot key. |
| **TKF\_INDICATOR**  0x00000020 | This flag is not implemented. |
| **TKF\_TOGGLEKEYSON**  0x00000001 | If this flag is set, the ToggleKeys feature is on. |

## Remarks

An application uses a **TOGGLEKEYS** structure when calling the [SystemParametersInfo](/en-us/windows/desktop/api/winuser/nf-winuser-systemparametersinfoa) function with the *uiAction* parameter set to **SPI\_GETTOGGLEKEYS** or **SPI\_SETTOGGLEKEYS**. When using SPI\_GETTOGGLEKEYS, an application must specify the **cbSize** member of the **TOGGLEKEYS** structure; the **SystemParametersInfo** function fills the remaining members. An application must specify all structure members when using the **SPI\_SETTOGGLEKEYS** value.

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
