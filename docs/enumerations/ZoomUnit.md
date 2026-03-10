# ZoomUnit

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/ne-uiautomationcore-zoomunit)

# ZoomUnit enumeration (uiautomationcore.h)

Contains possible values for the [IUIAutomationTransformPattern2::ZoomByUnit](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationtransformpattern2-zoombyunit) method, which zooms the viewport of a control by the specified unit.

## Syntax

```
typedef enum ZoomUnit {
  ZoomUnit_NoAmount = 0,
  ZoomUnit_LargeDecrement = 1,
  ZoomUnit_SmallDecrement = 2,
  ZoomUnit_LargeIncrement = 3,
  ZoomUnit_SmallIncrement = 4
} ;
```

## Constants

|  |
| --- |
| `ZoomUnit_NoAmount` Value: *0* No increase or decrease in zoom. |
| `ZoomUnit_LargeDecrement` Value: *1* Decrease zoom by a large decrement. |
| `ZoomUnit_SmallDecrement` Value: *2* Decrease zoom by a small decrement. |
| `ZoomUnit_LargeIncrement` Value: *3* Increase zoom by a large increment. |
| `ZoomUnit_SmallIncrement` Value: *4* Increase zoom by a small increment. |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 8 [desktop apps only] |
| **Minimum supported server** | Windows Server 2012 [desktop apps only] |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[IUIAutomationTransformPattern2::ZoomByUnit](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationtransformpattern2-zoombyunit)

---
