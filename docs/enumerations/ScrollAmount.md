# ScrollAmount

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/ne-uiautomationcore-scrollamount)

# ScrollAmount enumeration (uiautomationcore.h)

Contains values that specify the direction and distance to scroll.

## Syntax

```
typedef enum ScrollAmount {
  ScrollAmount_LargeDecrement = 0,
  ScrollAmount_SmallDecrement = 1,
  ScrollAmount_NoAmount = 2,
  ScrollAmount_LargeIncrement = 3,
  ScrollAmount_SmallIncrement = 4
} ;
```

## Constants

|  |
| --- |
| `ScrollAmount_LargeDecrement` Value: *0* Scrolling is done in large decrements, equivalent to pressing the PAGE UP key or clicking on a blank part of a scroll bar. If one page up is not a relevant amount for the control and no scroll bar exists, the value represents an amount equal to the current visible window. |
| `ScrollAmount_SmallDecrement` Value: *1* Scrolling is done in small decrements, equivalent to pressing an arrow key or clicking the arrow button on a scroll bar. |
| `ScrollAmount_NoAmount` Value: *2* No scrolling is done. |
| `ScrollAmount_LargeIncrement` Value: *3* Scrolling is done in large increments, equivalent to pressing the PAGE DOWN or PAGE UP key or clicking on a blank part of a scroll bar.   If one page is not a relevant amount for the control and no scroll bar exists, the value represents an amount equal to the current visible window. |
| `ScrollAmount_SmallIncrement` Value: *4* Scrolling is done in small increments, equivalent to pressing an arrow key or clicking the arrow   button on a scroll bar. |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps only] |
| **Minimum supported server** | Windows Server 2003 [desktop apps only] |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[IScrollProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-iscrollprovider)

---
