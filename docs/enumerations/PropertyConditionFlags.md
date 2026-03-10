# PropertyConditionFlags

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/ne-uiautomationcoreapi-propertyconditionflags)

# PropertyConditionFlags enumeration (uiautomationcoreapi.h)

Contains values used in creating property conditions.

## Syntax

```
typedef enum PropertyConditionFlags {
  PropertyConditionFlags_None = 0x00,
  PropertyConditionFlags_IgnoreCase = 0x01,
  PropertyConditionFlags_MatchSubstring = 0x02
} ;
```

## Constants

|  |
| --- |
| `PropertyConditionFlags_None` Value: *0x00* No flags. |
| `PropertyConditionFlags_IgnoreCase` Value: *0x01* Comparison of string properties is not case-sensitive. |
| `PropertyConditionFlags_MatchSubstring` Value: *0x02* [Windows 10 October 2018 Update (version 1809) and newer]  Comparison of substring properties is enabled. |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps only] |
| **Minimum supported server** | Windows Server 2003 [desktop apps only] |
| **Header** | uiautomationcoreapi.h (include UIAutomation.h, Uiautomationcoreapi.h) |

---
