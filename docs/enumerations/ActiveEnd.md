# ActiveEnd

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/ne-uiautomationcore-activeend)

# ActiveEnd enumeration (uiautomationcore.h)

Contains possible values for the [SelectionActiveEnd](/en-us/windows/desktop/WinAuto/uiauto-textattribute-ids) text attribute, which indicates the location of the caret relative to a text range that represents the currently selected text.

## Syntax

```
typedef enum ActiveEnd {
  ActiveEnd_None = 0,
  ActiveEnd_Start = 1,
  ActiveEnd_End = 2
} ;
```

## Constants

|  |
| --- |
| `ActiveEnd_None` Value: *0* The caret is not at either end of the text range. |
| `ActiveEnd_Start` Value: *1* The caret is at the beginning of the text range. |
| `ActiveEnd_End` Value: *2* The caret is at the end of the text range. |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 8 [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2012 [desktop apps | UWP apps] |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

---
