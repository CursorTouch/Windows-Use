# CaretPosition

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/ne-uiautomationcore-caretposition)

# CaretPosition enumeration (uiautomationcore.h)

Contains possible values for the [CaretPosition](/en-us/windows/desktop/WinAuto/uiauto-textattribute-ids) text attribute, which indicates the location of the caret relative to a line of text in a text range.

## Syntax

```
typedef enum CaretPosition {
  CaretPosition_Unknown = 0,
  CaretPosition_EndOfLine = 1,
  CaretPosition_BeginningOfLine = 2
} ;
```

## Constants

|  |
| --- |
| `CaretPosition_Unknown` Value: *0* The caret is not at the beginning or the end of a line. |
| `CaretPosition_EndOfLine` Value: *1* The caret is at the end of a line. |
| `CaretPosition_BeginningOfLine` Value: *2* The caret is at the beginning of a line. |

## Remarks

The provider of a text-based control considers the caret to be at some character position in the text. For example, if the caret is at the start of the text, it lies at position 0. If the caret is just after the first character, it lies at position 1, and so on. When text wraps around at the end of a line, typically a space is shown at the end of the line, and a non-space character at the start of the next line. The user might be able to place the caret after the space at the end of the first line, or before the non-space character at the start of the next line. However, both places are considered to be the same character position. The [CaretPosition](/en-us/windows/desktop/WinAuto/uiauto-textattribute-ids) attribute indicates whether the caret is shown at the end or the beginning of a line. If the caret lies at neither of these positions, the **CaretPosition** attribute is **CaretPosition\_Unknown**.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 8 [desktop apps only] |
| **Minimum supported server** | Windows Server 2012 [desktop apps only] |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

---
