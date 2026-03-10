# TreeTraversalOptions

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/ne-uiautomationcoreapi-treetraversaloptions)

# TreeTraversalOptions enumeration (uiautomationcoreapi.h)

Defines values that can be used to customize tree navigation order.

## Syntax

```
typedef enum TreeTraversalOptions {
  TreeTraversalOptions_Default = 0x0,
  TreeTraversalOptions_PostOrder = 0x1,
  TreeTraversalOptions_LastToFirstOrder = 0x2
} ;
```

## Constants

|  |
| --- |
| `TreeTraversalOptions_Default` Value: *0x0* Pre-order,  visit children from first to last. |
| `TreeTraversalOptions_PostOrder` Value: *0x1* Post-order, see Remarks for more info. |
| `TreeTraversalOptions_LastToFirstOrder` Value: *0x2* Visit children from last to first. |

## Remarks

Option groups (flags):

* Traversal order (pre-order, post-order) defines when nodes should be tested
  against search conditions. For example, "on enter" or "on leave".
* Visit order defines in which order relatives are visited. Relatives include
  children and siblings. Visit orders are relative to parents. From the child
  perspective First-to-Last means "visit the next sibling from the child" while
  Last-to-First means "visit the previous sibling from the child".

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 10, version 1703 [desktop apps only] |
| **Minimum supported server** | None supported |
| **Header** | uiautomationcoreapi.h (include UIAutomation.h, Uiautomationcoreapi.h) |

## See also

[Text Attribute Identifiers](/en-us/windows/desktop/WinAuto/uiauto-textattribute-ids)

---
