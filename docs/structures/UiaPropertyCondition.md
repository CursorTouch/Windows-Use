# UiaPropertyCondition

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/ns-uiautomationcoreapi-uiapropertycondition)

# UiaPropertyCondition structure (uiautomationcoreapi.h)

**Note**  This structure is deprecated.

Contains information about a condition used to find UI Automation elements that have a matching property.

## Syntax

```
struct UiaPropertyCondition {
  ConditionType          ConditionType;
  PROPERTYID             PropertyId;
  VARIANT                Value;
  PropertyConditionFlags Flags;
};
```

## Members

`ConditionType`

Type: **[ConditionType](/en-us/windows/desktop/api/uiautomationcoreapi/ne-uiautomationcoreapi-conditiontype)**

A value indicating the type of the condition.

`PropertyId`

Type: **PROPERTYID**

The identifier of the property to match. For a list of property IDs, see [Property Identifiers](/en-us/windows/desktop/WinAuto/uiauto-entry-propids).

`Value`

Type: **[VARIANT](/en-us/windows/desktop/WinAuto/variant-structure)**

The value that the property must have.

`Flags`

Type: **[PropertyConditionFlags](/en-us/windows/desktop/api/uiautomationclient/ne-uiautomationclient-propertyconditionflags)**

A value indicating how the condition is applied.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps only] |
| **Minimum supported server** | Windows Server 2003 [desktop apps only] |
| **Header** | uiautomationcoreapi.h |

---
