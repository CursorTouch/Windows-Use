# WindowVisualState

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/ne-uiautomationcore-windowvisualstate)

# WindowVisualState enumeration (uiautomationcore.h)

Contains values that specify the visual state of a window.

## Syntax

```
typedef enum WindowVisualState {
  WindowVisualState_Normal = 0,
  WindowVisualState_Maximized = 1,
  WindowVisualState_Minimized = 2
} ;
```

## Constants

|  |
| --- |
| `WindowVisualState_Normal` Value: *0* The window is normal (restored). |
| `WindowVisualState_Maximized` Value: *1* The window is maximized. |
| `WindowVisualState_Minimized` Value: *2* The window is minimized. |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps only] |
| **Minimum supported server** | Windows Server 2003 [desktop apps only] |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[IWindowProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-iwindowprovider)

---
