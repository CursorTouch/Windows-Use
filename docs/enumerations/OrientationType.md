# OrientationType

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/ne-uiautomationcore-orientationtype)

# OrientationType enumeration (uiautomationcore.h)

Contains values that specify the orientation of a control.

## Syntax

```
typedef enum OrientationType {
  OrientationType_None = 0,
  OrientationType_Horizontal = 1,
  OrientationType_Vertical = 2
} ;
```

## Constants

|  |
| --- |
| `OrientationType_None` Value: *0* The control has no orientation. |
| `OrientationType_Horizontal` Value: *1* The control has horizontal orientation. |
| `OrientationType_Vertical` Value: *2* The control has vertical orientation. |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2003 [desktop apps | UWP apps] |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[Text Attribute Identifiers](/en-us/windows/desktop/WinAuto/uiauto-textattribute-ids)

---
