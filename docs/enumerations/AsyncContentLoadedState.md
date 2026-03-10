# AsyncContentLoadedState

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/ne-uiautomationcoreapi-asynccontentloadedstate)

# AsyncContentLoadedState enumeration (uiautomationcoreapi.h)

Contains values that describe the progress of asynchronous loading of content.

## Syntax

```
typedef enum AsyncContentLoadedState {
  AsyncContentLoadedState_Beginning,
  AsyncContentLoadedState_Progress,
  AsyncContentLoadedState_Completed
} ;
```

## Constants

|  |
| --- |
| `AsyncContentLoadedState_Beginning` Loading of the content into the UI Automation element is beginning. |
| `AsyncContentLoadedState_Progress` Loading of the content into the UI Automation element is in progress. |
| `AsyncContentLoadedState_Completed` Loading of the content into the UI Automation element is complete. |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2003 [desktop apps | UWP apps] |
| **Header** | uiautomationcoreapi.h (include UIAutomation.h) |

---
