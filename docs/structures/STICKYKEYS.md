# STICKYKEYS

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-stickykeys)

# STICKYKEYS structure (winuser.h)

Contains information about the StickyKeys accessibility feature. When the StickyKeys feature is on, the user can press a modifier key (SHIFT, CTRL, or ALT) and then another key in sequence rather than at the same time, to enter shifted (modified) characters and other key combinations. Pressing a modifier key once *latches* the key down until the user presses a non-modifier key or clicks a mouse button. Pressing a modifier key twice *locks* the key until the user presses the key a third time.

## Syntax

```
typedef struct tagSTICKYKEYS {
  UINT  cbSize;
  DWORD dwFlags;
} STICKYKEYS, *LPSTICKYKEYS;
```

## Members

`cbSize`

Type: **[DWORD](/en-us/windows/desktop/WinProg/windows-data-types)**

Specifies the size, in bytes, of this structure.

`dwFlags`

Type: **[DWORD](/en-us/windows/desktop/WinProg/windows-data-types)**

A set of bit-flags that specify properties of the StickyKeys feature. The following bit-flag values are defined:

| Value | Meaning |
| --- | --- |
| **SKF\_AUDIBLEFEEDBACK**  0x00000040 | If this flag is set, the system plays a sound when the user latches, locks, or releases modifier keys using the StickyKeys feature. |
| **SKF\_AVAILABLE**  0x00000002 | If this flag is set, the StickyKeys feature is available. |
| **SKF\_CONFIRMHOTKEY**  0x00000008 | **Windows 95/98, Windows 2000:** A confirmation dialog appears when the StickyKeys feature is activated by using the hot key. |
| **SKF\_HOTKEYACTIVE**  0x00000004 | If this flag is set, the user can turn the StickyKeys feature on and off by pressing the SHIFT key five times. |
| **SKF\_HOTKEYSOUND**  0x00000010 | If this flag is set, the system plays a siren sound when the user turns the StickyKeys feature on or off by using the hot key. |
| **SKF\_INDICATOR**  0x00000020 | **Windows 95/98, Windows 2000:** A visual indicator should be displayed when the StickyKeys feature is on. |
| **SKF\_STICKYKEYSON**  0x00000001 | If this flag is set, the StickyKeys feature is on. |
| **SKF\_TRISTATE**  0x00000080 | If this flag is set, pressing a modifier key twice in a row locks down the key until the user presses it a third time. |
| **SKF\_TWOKEYSOFF**  0x00000100 | If this flag is set, releasing a modifier key that has been pressed in combination with any other key turns off the StickyKeys feature. |
| **SKF\_LALTLATCHED**  0x10000000 | **Windows 98, Windows 2000:** The left ALT key is latched. |
| **SKF\_LCTLLATCHED**  0x04000000 | **Windows 98, Windows 2000:**  The left CTRL key is latched. |
| **SKF\_LSHIFTLATCHED**  0x01000000 | **Windows 98, Windows 2000:**  The left SHIFT key is latched. |
| **SKF\_RALTLATCHED**  0x20000000 | **Windows 98, Windows 2000:**  The right ALT key is latched. |
| **SKF\_RCTLLATCHED**  0x08000000 | **Windows 98, Windows 2000:**  The right CTRL key is latched. |
| **SKF\_RSHIFTLATCHED**  0x02000000 | **Windows 98, Windows 2000:**  The right SHIFT key is latched. |
| **SKF\_LALTLOCKED**  0x00100000 | **Windows 98, Windows 2000:**  The left ALT key is locked. |
| **SKF\_LCTLLOCKED**  0x00040000 | **Windows 98, Windows 2000:**  The left CTRL key is locked. |
| **SKF\_LSHIFTLOCKED**  0x00010000 | **Windows 98, Windows 2000:**  The left SHIFT key is locked. |
| **SKF\_RALTLOCKED**  0x00200000 | **Windows 98, Windows 2000:**  The right ALT key is locked. |
| **SKF\_RCTLLOCKED**  0x00080000 | **Windows 98, Windows 2000:**  The right CTRL key is locked. |
| **SKF\_RSHIFTLOCKED**  0x00020000 | **Windows 98, Windows 2000:**  The right SHIFT key is locked. |
| **SKF\_LWINLATCHED**  0x40000000 | **Windows 98, Windows 2000:**  The left Windows key is latched. |
| **SKF\_RWINLATCHED**  0x80000000 | **Windows 98, Windows 2000:**  The right Windows key is latched. |
| **SKF\_LWINLOCKED**  0x00400000 | **Windows 98, Windows 2000:**  The left Windows key is locked. |
| **SKF\_RWINLOCKED**  0x00800000 | **Windows 98, Windows 2000:**  The right Windows key is locked. |

## Remarks

An application uses a **STICKYKEYS** structure when calling the [SystemParametersInfo](/en-us/windows/desktop/api/winuser/nf-winuser-systemparametersinfoa) function with the *uiAction* parameter set to **SPI\_GETSTICKYKEYS** or **SPI\_SETSTICKYKEYS**. When using **SPI\_GETSTICKYKEYS**, you must specify the **cbSize** member of the **STICKYKEYS** structure; the **SystemParametersInfo** function fills the remaining members. You must specify all structure members when using the **SPI\_SETSTICKYKEYS** value.

If you call [SystemParametersInfo](/en-us/windows/desktop/api/winuser/nf-winuser-systemparametersinfoa) with the **SPI\_SETSTICKYKEYS** value, the following flags are ignored:

* SKF\_LALTLATCHED
* SKF\_LCTLLATCHED
* SKF\_LSHIFTLATCHED
* SKF\_RALTLATCHED
* SKF\_RCTLLATCHED
* SKF\_RSHIFTLATCHED
* SKF\_LALTLOCKED
* SKF\_LCTLLOCKED
* SKF\_LSHIFTLOCKED
* SKF\_RALTLOCKED
* SKF\_RCTLLOCKED
* SKF\_RSHIFTLOCKED

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
