# FlowDirections

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/ne-uiautomationcore-flowdirections)

# FlowDirections enumeration (uiautomationcore.h)

Contains values for the TextFlowDirections text attribute.

## Syntax

```
typedef enum FlowDirections {
  FlowDirections_Default = 0,
  FlowDirections_RightToLeft = 0x1,
  FlowDirections_BottomToTop = 0x2,
  FlowDirections_Vertical = 0x4
} ;
```

## Constants

|  |
| --- |
| `FlowDirections_Default` Value: *0* The default flow direction. |
| `FlowDirections_RightToLeft` Value: *0x1* The text flows from right to left. |
| `FlowDirections_BottomToTop` Value: *0x2* The text flows from bottom to top. |
| `FlowDirections_Vertical` Value: *0x4* The text flows vertically. |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps only] |
| **Minimum supported server** | Windows Server 2003 [desktop apps only] |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[Text Attribute Identifiers](/en-us/windows/desktop/WinAuto/uiauto-textattribute-ids)

---
