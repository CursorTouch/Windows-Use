# UiaRect

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/ns-uiautomationcore-uiarect)

# UiaRect structure (uiautomationcore.h)

Contains the position and size of a rectangle, in screen coordinates.

## Syntax

```
struct UiaRect {
  double left;
  double top;
  double width;
  double height;
};
```

## Members

`left`

Type: **double**

Position of the left side.

`top`

Type: **double**

Position of the top side.

`width`

Type: **double**

Width.

`height`

Type: **double**

Height.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2003 [desktop apps | UWP apps] |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

---
