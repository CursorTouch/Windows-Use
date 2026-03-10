# ExpandCollapseState

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/ne-uiautomationcore-expandcollapsestate)

# ExpandCollapseState enumeration (uiautomationcore.h)

Contains values that specify the state of a UI element that can be expanded and collapsed.

## Syntax

```
typedef enum ExpandCollapseState {
  ExpandCollapseState_Collapsed = 0,
  ExpandCollapseState_Expanded = 1,
  ExpandCollapseState_PartiallyExpanded = 2,
  ExpandCollapseState_LeafNode = 3
} ;
```

## Constants

|  |
| --- |
| `ExpandCollapseState_Collapsed` Value: *0* No children are visible. |
| `ExpandCollapseState_Expanded` Value: *1* All children are visible. |
| `ExpandCollapseState_PartiallyExpanded` Value: *2* Some, but not all, children are visible. |
| `ExpandCollapseState_LeafNode` Value: *3* The element does not expand or collapse. |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps only] |
| **Minimum supported server** | Windows Server 2003 [desktop apps only] |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[IExpandCollapseProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-iexpandcollapseprovider)

---
