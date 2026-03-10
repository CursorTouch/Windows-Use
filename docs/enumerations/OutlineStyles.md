# OutlineStyles

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/ne-uiautomationcore-outlinestyles)

# OutlineStyles enumeration (uiautomationcore.h)

Contains values for the OutlineStyle text attribute.

## Syntax

```
typedef enum OutlineStyles {
  OutlineStyles_None = 0,
  OutlineStyles_Outline = 1,
  OutlineStyles_Shadow = 2,
  OutlineStyles_Engraved = 4,
  OutlineStyles_Embossed = 8
} ;
```

## Constants

|  |
| --- |
| `OutlineStyles_None` Value: *0* No outline style. |
| `OutlineStyles_Outline` Value: *1* A simple outline. |
| `OutlineStyles_Shadow` Value: *2* A shadow. |
| `OutlineStyles_Engraved` Value: *4* An engraved appearance. |
| `OutlineStyles_Embossed` Value: *8* An embossed appearance. |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps only] |
| **Minimum supported server** | Windows Server 2003 [desktop apps only] |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[Text Attribute Identifiers](/en-us/windows/desktop/WinAuto/uiauto-textattribute-ids)

---
