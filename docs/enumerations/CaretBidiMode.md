# CaretBidiMode

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/ne-uiautomationcore-caretbidimode)

# CaretBidiMode enumeration (uiautomationcore.h)

Contains possible values for the [CaretBidiMode](/en-us/windows/desktop/WinAuto/uiauto-textattribute-ids) text attribute, which indicates whether the caret is in text that flows from left to right, or from right to left.

## Syntax

```
typedef enum CaretBidiMode {
  CaretBidiMode_LTR = 0,
  CaretBidiMode_RTL = 1
} ;
```

## Constants

|  |
| --- |
| `CaretBidiMode_LTR` Value: *0* The caret is in text that flows from left to right. |
| `CaretBidiMode_RTL` Value: *1* The caret is in text that flows from right to left. |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 8 [desktop apps only] |
| **Minimum supported server** | Windows Server 2012 [desktop apps only] |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

---
