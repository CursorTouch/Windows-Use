# ConditionType

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/ne-uiautomationcoreapi-conditiontype)

# ConditionType enumeration (uiautomationcoreapi.h)

Contains values that specify a type of [UiaCondition](/en-us/windows/desktop/api/uiautomationcoreapi/ns-uiautomationcoreapi-uiacondition).

## Syntax

```
typedef enum ConditionType {
  ConditionType_True = 0,
  ConditionType_False = 1,
  ConditionType_Property = 2,
  ConditionType_And = 3,
  ConditionType_Or = 4,
  ConditionType_Not = 5
} ;
```

## Constants

|  |
| --- |
| `ConditionType_True` Value: *0* A condition that is true. |
| `ConditionType_False` Value: *1* A condition that is false. |
| `ConditionType_Property` Value: *2* A property condition. |
| `ConditionType_And` Value: *3* A complex condition where all the contained conditions must be true. |
| `ConditionType_Or` Value: *4* A complex condition where at least one of the contained conditions must be true. |
| `ConditionType_Not` Value: *5* A condition that is true if the specified conditions are not met. |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps only] |
| **Minimum supported server** | Windows Server 2003 [desktop apps only] |
| **Header** | uiautomationcoreapi.h (include UIAutomation.h) |

---
