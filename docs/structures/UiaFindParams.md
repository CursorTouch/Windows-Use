# UiaFindParams

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/ns-uiautomationcoreapi-uiafindparams)

# UiaFindParams structure (uiautomationcoreapi.h)

**Note**  This structure is deprecated.

Contains parameters used in the [UiaFind](/en-us/windows/desktop/api/uiautomationcoreapi/nf-uiautomationcoreapi-uiafind) function.

## Syntax

```
struct UiaFindParams {
  int                 MaxDepth;
  BOOL                FindFirst;
  BOOL                ExcludeRoot;
  struct UiaCondition *pFindCondition;
};
```

## Members

`MaxDepth`

Type: **int**

The maximum depth to which to search the tree for matching elements.

`FindFirst`

Type: **[BOOL](/en-us/windows/desktop/WinProg/windows-data-types)**

**TRUE** to return only the first matching element; **FALSE** to return all matching elements.

`ExcludeRoot`

Type: **[BOOL](/en-us/windows/desktop/WinProg/windows-data-types)**

**TRUE** to exclude the root element; otherwise **FALSE**.

`pFindCondition`

Type: **[UiaCondition](/en-us/windows/desktop/api/uiautomationcoreapi/ns-uiautomationcoreapi-uiacondition)\***

Pointer to a [UiaCondition](/en-us/windows/desktop/api/uiautomationcoreapi/ns-uiautomationcoreapi-uiacondition) structure that contains information about a condition that returned elements must match.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps only] |
| **Minimum supported server** | Windows Server 2003 [desktop apps only] |
| **Header** | uiautomationcoreapi.h |

---
