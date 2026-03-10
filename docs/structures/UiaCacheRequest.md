# UiaCacheRequest

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/ns-uiautomationcoreapi-uiacacherequest)

# UiaCacheRequest structure (uiautomationcoreapi.h)

**Note**  This structure is deprecated.

Contains information about a request to cache data about UI Automation elements.

## Syntax

```
struct UiaCacheRequest {
  struct UiaCondition   *pViewCondition;
  TreeScope             Scope;
  PROPERTYID            *pProperties;
  int                   cProperties;
  PATTERNID             *pPatterns;
  int                   cPatterns;
  AutomationElementMode automationElementMode;
};
```

## Members

`pViewCondition`

Type: **UiaCondition \***

The address of a [UiaCondition](/en-us/windows/desktop/api/uiautomationcoreapi/ns-uiautomationcoreapi-uiacondition) structure that specifies the condition that cached elements must match.

`Scope`

Type: **[TreeScope](/en-us/windows/desktop/api/uiautomationclient/ne-uiautomationclient-treescope)**

A value from the [TreeScope](/en-us/windows/desktop/api/uiautomationclient/ne-uiautomationclient-treescope) enumerated type indicating the scope of the cache request; for example, whether it includes children of the root element.

`pProperties`

Type: **PROPERTYID\***

The address of an array of identifiers for properties to cache. For a list of property IDs, see [Property Identifiers](/en-us/windows/desktop/WinAuto/uiauto-entry-propids).

`cProperties`

Type: **int**

The count of elements in the **pProperties** array.

`pPatterns`

Type: **PATTERNID\***

The address of an array of identifiers for control patterns to cache. For a list of control pattern IDs, see [Control Pattern Identifiers](/en-us/windows/desktop/WinAuto/uiauto-controlpattern-ids).

`cPatterns`

Type: **int**

The count of elements in the **pPatterns** array.

`automationElementMode`

Type: **[AutomationElementMode](/en-us/windows/desktop/api/uiautomationclient/ne-uiautomationclient-automationelementmode)**

A value from the [AutomationElementMode](/en-us/windows/desktop/api/uiautomationclient/ne-uiautomationclient-automationelementmode) enumerated type indicating the type of reference to cached UI Automation elements that is to be returned.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps only] |
| **Minimum supported server** | Windows Server 2003 [desktop apps only] |
| **Header** | uiautomationcoreapi.h |

---
