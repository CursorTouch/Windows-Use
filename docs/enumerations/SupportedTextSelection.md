# SupportedTextSelection

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/ne-uiautomationcore-supportedtextselection)

# SupportedTextSelection enumeration (uiautomationcore.h)

Contains values that specify the supported text selection attribute.

## Syntax

```
typedef enum SupportedTextSelection {
  SupportedTextSelection_None = 0,
  SupportedTextSelection_Single = 1,
  SupportedTextSelection_Multiple = 2
} ;
```

## Constants

|  |
| --- |
| `SupportedTextSelection_None` Value: *0* Does not support text selections. |
| `SupportedTextSelection_Single` Value: *1* Supports a single, continuous text selection. |
| `SupportedTextSelection_Multiple` Value: *2* Supports multiple, disjoint text selections. |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps only] |
| **Minimum supported server** | Windows Server 2003 [desktop apps only] |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[Text Attribute Identifiers](/en-us/windows/desktop/WinAuto/uiauto-textattribute-ids)

---
