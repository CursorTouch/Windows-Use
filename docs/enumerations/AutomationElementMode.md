# AutomationElementMode

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/ne-uiautomationcoreapi-automationelementmode)

# AutomationElementMode enumeration (uiautomationcoreapi.h)

Contains values that specify the type of reference to use when returning UI Automation elements.

## Syntax

```
typedef enum AutomationElementMode {
  AutomationElementMode_None,
  AutomationElementMode_Full
} ;
```

## Constants

|  |
| --- |
| `AutomationElementMode_None` Specifies that returned elements have no reference to the underlying UI and contain only cached information. |
| `AutomationElementMode_Full` Specifies that returned elements have a full reference to the underlying UI. |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps only] |
| **Minimum supported server** | Windows Server 2003 [desktop apps only] |
| **Header** | uiautomationcoreapi.h (include UIAutomation.h, Uiautomationcoreapi.h) |

---
