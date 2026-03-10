# DockPosition

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/ne-uiautomationcore-dockposition)

# DockPosition enumeration (uiautomationcore.h)

Contains values that specify the location of a docking window represented by the [Dock](/en-us/windows/desktop/WinAuto/uiauto-implementingdock) *control pattern*.

## Syntax

```
typedef enum DockPosition {
  DockPosition_Top = 0,
  DockPosition_Left = 1,
  DockPosition_Bottom = 2,
  DockPosition_Right = 3,
  DockPosition_Fill = 4,
  DockPosition_None = 5
} ;
```

## Constants

|  |
| --- |
| `DockPosition_Top` Value: *0* The window is docked at the top. |
| `DockPosition_Left` Value: *1* The window is docked at the left. |
| `DockPosition_Bottom` Value: *2* The window is docked at the bottom. |
| `DockPosition_Right` Value: *3* The window is docked at the right. |
| `DockPosition_Fill` Value: *4* The window is docked on all four sides. |
| `DockPosition_None` Value: *5* The window is not docked. |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps only] |
| **Minimum supported server** | Windows Server 2003 [desktop apps only] |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[IDockProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-idockprovider)

---
