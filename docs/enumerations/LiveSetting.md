# LiveSetting

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/ne-uiautomationcore-livesetting)

# LiveSetting enumeration (uiautomationcore.h)

Contains possible values for the LiveSetting property. This property is implemented by provider elements that are part of a live region.

## Syntax

```
typedef enum LiveSetting {
  Off = 0,
  Polite = 1,
  Assertive = 2
} ;
```

## Constants

|  |
| --- |
| `Off` Value: *0* |
| `Polite` Value: *1* |
| `Assertive` Value: *2* |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 8 [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2012 [desktop apps | UWP apps] |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[CachedLiveSetting](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement2-get_cachedlivesetting)

[CurrentLiveSetting](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement2-get_currentlivesetting)

---
