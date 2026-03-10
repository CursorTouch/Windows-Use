# TextDecorationLineStyle

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/ne-uiautomationcore-textdecorationlinestyle)

# TextDecorationLineStyle enumeration (uiautomationcore.h)

Contains values that specify the OverlineStyle, StrikethroughStyle, and UnderlineStyle text attributes.

## Syntax

```
typedef enum TextDecorationLineStyle {
  TextDecorationLineStyle_None = 0,
  TextDecorationLineStyle_Single = 1,
  TextDecorationLineStyle_WordsOnly = 2,
  TextDecorationLineStyle_Double = 3,
  TextDecorationLineStyle_Dot = 4,
  TextDecorationLineStyle_Dash = 5,
  TextDecorationLineStyle_DashDot = 6,
  TextDecorationLineStyle_DashDotDot = 7,
  TextDecorationLineStyle_Wavy = 8,
  TextDecorationLineStyle_ThickSingle = 9,
  TextDecorationLineStyle_DoubleWavy = 11,
  TextDecorationLineStyle_ThickWavy = 12,
  TextDecorationLineStyle_LongDash = 13,
  TextDecorationLineStyle_ThickDash = 14,
  TextDecorationLineStyle_ThickDashDot = 15,
  TextDecorationLineStyle_ThickDashDotDot = 16,
  TextDecorationLineStyle_ThickDot = 17,
  TextDecorationLineStyle_ThickLongDash = 18,
  TextDecorationLineStyle_Other = -1
} ;
```

## Constants

|  |
| --- |
| `TextDecorationLineStyle_None` Value: *0* No line style. |
| `TextDecorationLineStyle_Single` Value: *1* A single solid line. |
| `TextDecorationLineStyle_WordsOnly` Value: *2* Only words (not spaces) are underlined. |
| `TextDecorationLineStyle_Double` Value: *3* A double line. |
| `TextDecorationLineStyle_Dot` Value: *4* A dotted line. |
| `TextDecorationLineStyle_Dash` Value: *5* A dashed line. |
| `TextDecorationLineStyle_DashDot` Value: *6* Alternating dashes and dots. |
| `TextDecorationLineStyle_DashDotDot` Value: *7* A dash followed by two dots. |
| `TextDecorationLineStyle_Wavy` Value: *8* A wavy line. |
| `TextDecorationLineStyle_ThickSingle` Value: *9* A thick single line. |
| `TextDecorationLineStyle_DoubleWavy` Value: *11* A double wavy line. |
| `TextDecorationLineStyle_ThickWavy` Value: *12* A thick wavy line. |
| `TextDecorationLineStyle_LongDash` Value: *13* Long dashes. |
| `TextDecorationLineStyle_ThickDash` Value: *14* A thick dashed line. |
| `TextDecorationLineStyle_ThickDashDot` Value: *15* Thick dashes alternating with thick dots. |
| `TextDecorationLineStyle_ThickDashDotDot` Value: *16* A thick dash followed by two thick dots. |
| `TextDecorationLineStyle_ThickDot` Value: *17* A thick dotted line. |
| `TextDecorationLineStyle_ThickLongDash` Value: *18* Thick long dashes. |
| `TextDecorationLineStyle_Other` Value: *-1* A line style not represented by another value. |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps only] |
| **Minimum supported server** | Windows Server 2003 [desktop apps only] |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[Text Attribute Identifiers](/en-us/windows/desktop/WinAuto/uiauto-textattribute-ids)

---
