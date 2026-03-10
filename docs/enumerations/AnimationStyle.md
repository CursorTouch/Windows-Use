# AnimationStyle

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/ne-uiautomationcore-animationstyle)

# AnimationStyle enumeration (uiautomationcore.h)

Contains values for the AnimationStyle text attribute.

## Syntax

```
typedef enum AnimationStyle {
  AnimationStyle_None = 0,
  AnimationStyle_LasVegasLights = 1,
  AnimationStyle_BlinkingBackground = 2,
  AnimationStyle_SparkleText = 3,
  AnimationStyle_MarchingBlackAnts = 4,
  AnimationStyle_MarchingRedAnts = 5,
  AnimationStyle_Shimmer = 6,
  AnimationStyle_Other = -1
} ;
```

## Constants

|  |
| --- |
| `AnimationStyle_None` Value: *0* None. |
| `AnimationStyle_LasVegasLights` Value: *1* The bounding rectangle displays a border of alternating icons of different colors. |
| `AnimationStyle_BlinkingBackground` Value: *2* The font and background alternate between assigned colors and contrasting colors. |
| `AnimationStyle_SparkleText` Value: *3* The background displays flashing, multicolored icons. |
| `AnimationStyle_MarchingBlackAnts` Value: *4* The bounding rectangle displays moving black dashes. |
| `AnimationStyle_MarchingRedAnts` Value: *5* The bounding rectangle displays moving red dashes. |
| `AnimationStyle_Shimmer` Value: *6* The font alternates between solid and blurred. |
| `AnimationStyle_Other` Value: *-1* Other. |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps only] |
| **Minimum supported server** | Windows Server 2003 [desktop apps only] |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[Text Attribute Identifiers](/en-us/windows/desktop/WinAuto/uiauto-textattribute-ids)

---
