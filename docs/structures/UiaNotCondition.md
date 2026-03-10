# UiaNotCondition

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/ns-uiautomationcoreapi-uianotcondition)

# UiaNotCondition structure (uiautomationcoreapi.h)

**Note**  This structure is deprecated.

Contains information about a negative condition.

## Syntax

```
struct UiaNotCondition {
  ConditionType       ConditionType;
  struct UiaCondition *pCondition;
};
```

## Members

`ConditionType`

Type: **[ConditionType](/en-us/windows/desktop/api/uiautomationcoreapi/ne-uiautomationcoreapi-conditiontype)**

A value from the [ConditionType](/en-us/windows/desktop/api/uiautomationcoreapi/ne-uiautomationcoreapi-conditiontype) enumerated type indicating the type of condition.

`pCondition`

Type: **[UiaCondition](/en-us/windows/desktop/api/uiautomationcoreapi/ns-uiautomationcoreapi-uiacondition)\***

The address of a [UiaCondition](/en-us/windows/desktop/api/uiautomationcoreapi/ns-uiautomationcoreapi-uiacondition) structure containing information about the condition.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps only] |
| **Minimum supported server** | Windows Server 2003 [desktop apps only] |
| **Header** | uiautomationcoreapi.h |

---
