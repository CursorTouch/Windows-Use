# FillType

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/ne-uiautomationcore-filltype)

# FillType enumeration (uiautomationcore.h)

Contains values for the FillType attribute.

## Syntax

```
typedef enum FillType {
  FillType_None = 0,
  FillType_Color = 1,
  FillType_Gradient = 2,
  FillType_Picture = 3,
  FillType_Pattern = 4
} ;
```

## Constants

|  |
| --- |
| `FillType_None` Value: *0* The element is not filled. |
| `FillType_Color` Value: *1* The element is filled with a solid color. |
| `FillType_Gradient` Value: *2* The element is filled with a gradient. |
| `FillType_Picture` Value: *3* The element is filled using a picture. |
| `FillType_Pattern` Value: *4* The element is filled using a pattern. |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 10, version 1703 [desktop apps only] |
| **Minimum supported server** | Windows Server 2016 [desktop apps only] |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[VisualEffects](/en-us/windows/desktop/api/uiautomationcore/ne-uiautomationcore-visualeffects)

---
