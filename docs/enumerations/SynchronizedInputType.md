# SynchronizedInputType

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/ne-uiautomationcore-synchronizedinputtype)

# SynchronizedInputType enumeration (uiautomationcore.h)

Contains values that specify the type of synchronized input.

## Syntax

```
typedef enum SynchronizedInputType {
  SynchronizedInputType_KeyUp = 0x1,
  SynchronizedInputType_KeyDown = 0x2,
  SynchronizedInputType_LeftMouseUp = 0x4,
  SynchronizedInputType_LeftMouseDown = 0x8,
  SynchronizedInputType_RightMouseUp = 0x10,
  SynchronizedInputType_RightMouseDown = 0x20
} ;
```

## Constants

|  |
| --- |
| `SynchronizedInputType_KeyUp` Value: *0x1* A key has been released. |
| `SynchronizedInputType_KeyDown` Value: *0x2* A key has been pressed. |
| `SynchronizedInputType_LeftMouseUp` Value: *0x4* The left mouse button has been released. |
| `SynchronizedInputType_LeftMouseDown` Value: *0x8* The left mouse button has been pressed. |
| `SynchronizedInputType_RightMouseUp` Value: *0x10* The right mouse button has been released. |
| `SynchronizedInputType_RightMouseDown` Value: *0x20* The right mouse button has been pressed. |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps | UWP apps] |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

---
