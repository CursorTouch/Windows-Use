# SERIALKEYSA

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-serialkeysa)

# SERIALKEYSA structure (winuser.h)

Contains information about the SerialKeys accessibility feature, which interprets data from a communication aid attached to a serial port as commands causing the system to simulate keyboard and mouse input.

## Syntax

```
typedef struct tagSERIALKEYSA {
  UINT  cbSize;
  DWORD dwFlags;
  LPSTR lpszActivePort;
  LPSTR lpszPort;
  UINT  iBaudRate;
  UINT  iPortState;
  UINT  iActive;
} SERIALKEYSA, *LPSERIALKEYSA;
```

## Members

`cbSize`

Type: **[UINT](/en-us/windows/desktop/WinProg/windows-data-types)**

Specifies the structure size, in bytes.

`dwFlags`

Type: **[DWORD](/en-us/windows/desktop/WinProg/windows-data-types)**

Specifies a combination of the following values:

| Value | Meaning |
| --- | --- |
| **SERKF\_AVAILABLE**  0x00000002 | The SerialKeys feature is available. |
| **SERKF\_INDICATOR**  0x00000004 | A visual indicator is displayed when the SerialKeys feature is on. This value is not currently used and is ignored. |
| **SERKF\_SERIALKEYSON**  0x00000001 | The SerialKeys feature is on. |

`lpszActivePort`

Type: **[LPSTR](/en-us/windows/desktop/WinProg/windows-data-types)**

Points to a string that contains the name of the serial port that receives input from the communication aid when the SerialKeys feature is on. If no port is being used, this member is **NULL**. If this member is "Auto", the system watches all unused serial ports for input from communication aids.

`lpszPort`

Type: **[LPSTR](/en-us/windows/desktop/WinProg/windows-data-types)**

Reserved; must be **NULL**.

`iBaudRate`

Type: **[UINT](/en-us/windows/desktop/WinProg/windows-data-types)**

Specifies the baud rate setting for the serial port specified by the **lpszActivePort** member. This member should be set to one of the CBR\_ values defined in the winbase.h header file. If **lpszActivePort** is **NULL**, this member is zero.

`iPortState`

Type: **[UINT](/en-us/windows/desktop/WinProg/windows-data-types)**

Specifies the state of the port specified by the **lpszActivePort** member. If **lpszActivePort** is **NULL**, **iPortState** is zero; otherwise, it is one of the following values:

| Value | Meaning |
| --- | --- |
| 0 | All input on this port is ignored by the SerialKeys feature. |
| 1 | Input on this port is watched for SerialKeys activation sequences when no other application has the port open. |
| 2 | All input on this port is treated as SerialKeys commands. |

`iActive`

Type: **[UINT](/en-us/windows/desktop/WinProg/windows-data-types)**

Specifies the active port.

## Remarks

An application uses this structure when calling the [SystemParametersInfo](/en-us/windows/desktop/api/winuser/nf-winuser-systemparametersinfoa) function with the **SPI\_GETSERIALKEYS** or **SPI\_SETSERIALKEYS** value. When using **SPI\_GETSERIALKEYS**, an application must specify the **cbSize**, **lpszActivePort**, and **lpszPort** members of the **SERIALKEYS** structure; the **SystemParametersInfo** function fills the remaining members. An application must specify all structure members when using the **SPI\_SETSERIALKEYS** value.

Note

The winuser.h header defines SERIALKEYS as an alias that automatically selects the ANSI or Unicode version of this function based on the definition of the UNICODE preprocessor constant. Mixing usage of the encoding-neutral alias with code that is not encoding-neutral can lead to mismatches that result in compilation or runtime errors. For more information, see [Conventions for Function Prototypes](/en-us/windows/win32/intl/conventions-for-function-prototypes).

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
