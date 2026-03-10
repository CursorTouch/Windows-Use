# NormalizeState

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/ne-uiautomationcoreapi-normalizestate)

# NormalizeState enumeration (uiautomationcoreapi.h)

Contains values that specify the behavior of [UiaGetUpdatedCache](/en-us/windows/desktop/api/uiautomationcoreapi/nf-uiautomationcoreapi-uiagetupdatedcache).

## Syntax

```
typedef enum NormalizeState {
  NormalizeState_None,
  NormalizeState_View,
  NormalizeState_Custom
} ;
```

## Constants

|  |
| --- |
| `NormalizeState_None` No normalization. |
| `NormalizeState_View` Normalize against the condition in the cache request specified by pRequest. |
| `NormalizeState_Custom` Normalize against the condition specified in pNormalizeCondition. |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps only] |
| **Minimum supported server** | Windows Server 2003 [desktop apps only] |
| **Header** | uiautomationcoreapi.h (include UIAutomation.h) |

---
