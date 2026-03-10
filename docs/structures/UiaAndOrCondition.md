# UiaAndOrCondition

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/ns-uiautomationcoreapi-uiaandorcondition)

# UiaAndOrCondition structure (uiautomationcoreapi.h)

**Note**  This structure is deprecated.

Contains information about a complex condition.

## Syntax

```
struct UiaAndOrCondition {
  ConditionType ConditionType;
  UiaCondition  **ppConditions;
  struct        UiaCondition;
  int           cConditions;
};
```

## Members

`ConditionType`

Type: **[ConditionType](/en-us/windows/desktop/api/uiautomationcoreapi/ne-uiautomationcoreapi-conditiontype)**

A value from the [ConditionType](/en-us/windows/desktop/api/uiautomationcoreapi/ne-uiautomationcoreapi-conditiontype) enumerated type indicating the type of the condition.

`ppConditions`

Type: **[UiaCondition](/en-us/windows/desktop/api/uiautomationcoreapi/ns-uiautomationcoreapi-uiacondition)\*\***

The address of an array of pointers to [UiaCondition](/en-us/windows/desktop/api/uiautomationcoreapi/ns-uiautomationcoreapi-uiacondition) structures containing information about the complex condition.

`UiaCondition`

`cConditions`

Type: **int**

The count of elements in the **ppConditions** array.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps only] |
| **Minimum supported server** | Windows Server 2003 [desktop apps only] |
| **Header** | uiautomationcoreapi.h |

---
