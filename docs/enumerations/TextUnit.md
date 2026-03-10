# TextUnit

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/ne-uiautomationcore-textunit)

# TextUnit enumeration (uiautomationcore.h)

Contains values that specify units of text for the purposes of navigation.

## Syntax

```
typedef enum TextUnit {
  TextUnit_Character = 0,
  TextUnit_Format = 1,
  TextUnit_Word = 2,
  TextUnit_Line = 3,
  TextUnit_Paragraph = 4,
  TextUnit_Page = 5,
  TextUnit_Document = 6
} ;
```

## Constants

|  |
| --- |
| `TextUnit_Character` Value: *0* Character. |
| `TextUnit_Format` Value: *1* Format. |
| `TextUnit_Word` Value: *2* Word. |
| `TextUnit_Line` Value: *3* Line. |
| `TextUnit_Paragraph` Value: *4* Paragraph. |
| `TextUnit_Page` Value: *5* Page. |
| `TextUnit_Document` Value: *6* Document. |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps only] |
| **Minimum supported server** | Windows Server 2003 [desktop apps only] |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[Text Attribute Identifiers](/en-us/windows/desktop/WinAuto/uiauto-textattribute-ids)

---
