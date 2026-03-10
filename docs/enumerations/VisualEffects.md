# VisualEffects

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/ne-uiautomationcore-visualeffects)

# VisualEffects enumeration (uiautomationcore.h)

Contains values for the VisualEffects attribute.

## Syntax

```
typedef enum VisualEffects {
  VisualEffects_None = 0,
  VisualEffects_Shadow,
  VisualEffects_Reflection,
  VisualEffects_Glow,
  VisualEffects_SoftEdges,
  VisualEffects_Bevel
} ;
```

## Constants

|  |
| --- |
| `VisualEffects_None` Value: *0* No visual effects |
| `VisualEffects_Shadow` Shadow effect |
| `VisualEffects_Reflection` Reflection effect |
| `VisualEffects_Glow` Glow effect |
| `VisualEffects_SoftEdges` Soft edges effect |
| `VisualEffects_Bevel` Bevel effect |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 10, version 1703 [desktop apps only] |
| **Minimum supported server** | Windows Server 2016 [desktop apps only] |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[FillType](/en-us/windows/desktop/api/uiautomationcore/ne-uiautomationcore-filltype)

---
