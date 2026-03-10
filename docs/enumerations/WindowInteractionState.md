# WindowInteractionState

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/ne-uiautomationcore-windowinteractionstate)

# WindowInteractionState enumeration (uiautomationcore.h)

Contains values that specify the current state of the window for purposes of user interaction.

## Syntax

```
typedef enum WindowInteractionState {
  WindowInteractionState_Running = 0,
  WindowInteractionState_Closing = 1,
  WindowInteractionState_ReadyForUserInteraction = 2,
  WindowInteractionState_BlockedByModalWindow = 3,
  WindowInteractionState_NotResponding = 4
} ;
```

## Constants

|  |
| --- |
| `WindowInteractionState_Running` Value: *0* The window is running. This does not guarantee that the window is ready for user interaction or is responding. |
| `WindowInteractionState_Closing` Value: *1* The window is closing. |
| `WindowInteractionState_ReadyForUserInteraction` Value: *2* The window is ready for user interaction. |
| `WindowInteractionState_BlockedByModalWindow` Value: *3* The window is blocked by a modal window. |
| `WindowInteractionState_NotResponding` Value: *4* The window is not responding. |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps only] |
| **Minimum supported server** | Windows Server 2003 [desktop apps only] |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[IWindowProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-iwindowprovider)

---
