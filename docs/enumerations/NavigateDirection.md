# NavigateDirection

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/ne-uiautomationcore-navigatedirection)

# NavigateDirection enumeration (uiautomationcore.h)

Contains values used to specify the direction of navigation within the Microsoft UI Automation tree.

## Syntax

```
typedef enum NavigateDirection {
  NavigateDirection_Parent = 0,
  NavigateDirection_NextSibling = 1,
  NavigateDirection_PreviousSibling = 2,
  NavigateDirection_FirstChild = 3,
  NavigateDirection_LastChild = 4
} ;
```

## Constants

|  |
| --- |
| `NavigateDirection_Parent` Value: *0* The navigation direction is to the parent. |
| `NavigateDirection_NextSibling` Value: *1* The navigation direction is to the next sibling. |
| `NavigateDirection_PreviousSibling` Value: *2* The navigation direction is to the previous sibling. |
| `NavigateDirection_FirstChild` Value: *3* The navigation direction is to the first child. |
| `NavigateDirection_LastChild` Value: *4* The navigation direction is to the last child. |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2003 [desktop apps | UWP apps] |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[Navigate](/en-us/windows/desktop/api/uiautomationcore/nf-uiautomationcore-irawelementproviderfragment-navigate)

---
