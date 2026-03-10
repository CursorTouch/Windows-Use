# UIAutomationType

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/ne-uiautomationcore-uiautomationtype)

# UIAutomationType enumeration (uiautomationcore.h)

Contains values used to indicate Microsoft UI Automation data types.

## Syntax

```
typedef enum UIAutomationType {
  UIAutomationType_Int = 0x1,
  UIAutomationType_Bool = 0x2,
  UIAutomationType_String = 0x3,
  UIAutomationType_Double = 0x4,
  UIAutomationType_Point = 0x5,
  UIAutomationType_Rect = 0x6,
  UIAutomationType_Element = 0x7,
  UIAutomationType_Array = 0x10000,
  UIAutomationType_Out = 0x20000,
  UIAutomationType_IntArray,
  UIAutomationType_BoolArray,
  UIAutomationType_StringArray,
  UIAutomationType_DoubleArray,
  UIAutomationType_PointArray,
  UIAutomationType_RectArray,
  UIAutomationType_ElementArray,
  UIAutomationType_OutInt,
  UIAutomationType_OutBool,
  UIAutomationType_OutString,
  UIAutomationType_OutDouble,
  UIAutomationType_OutPoint,
  UIAutomationType_OutRect,
  UIAutomationType_OutElement,
  UIAutomationType_OutIntArray,
  UIAutomationType_OutBoolArray,
  UIAutomationType_OutStringArray,
  UIAutomationType_OutDoubleArray,
  UIAutomationType_OutPointArray,
  UIAutomationType_OutRectArray,
  UIAutomationType_OutElementArray
} ;
```

## Constants

|  |
| --- |
| `UIAutomationType_Int` Value: *0x1* An integer. |
| `UIAutomationType_Bool` Value: *0x2* An Boolean value. |
| `UIAutomationType_String` Value: *0x3* A null-terminated character string. |
| `UIAutomationType_Double` Value: *0x4* A double-precision floating-point number. |
| `UIAutomationType_Point` Value: *0x5* A [POINT](/en-us/windows/win32/api/windef/ns-windef-point) structure containing the x- and y-coordinates of a point. |
| `UIAutomationType_Rect` Value: *0x6* A [RECT](/en-us/windows/desktop/api/windef/ns-windef-rect) structure containing the coordinates of the upper-left and lower-right corners of a rectangle. This type is not supported for a custom UI Automation property. |
| `UIAutomationType_Element` Value: *0x7* The address of the [IUIAutomationElement](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationelement) interface of a UI Automation element. |
| `UIAutomationType_Array` Value: *0x10000* An array of an unspecified type. |
| `UIAutomationType_Out` Value: *0x20000* The address of a variable that receives a value retrieved by a function. |
| `UIAutomationType_IntArray` An array of integers. This type is not supported for a custom UI Automation property. |
| `UIAutomationType_BoolArray` An array of Boolean values. This type is not supported for a custom UI Automation property. |
| `UIAutomationType_StringArray` An array of null-terminated character strings. This type is not supported for a custom UI Automation property. |
| `UIAutomationType_DoubleArray` An array of double-precision floating-point numbers. This type is not supported for a custom UI Automation property. |
| `UIAutomationType_PointArray` An array of [POINT](/en-us/windows/win32/api/windef/ns-windef-point) structures, each containing the x- and y-coordinates of a point. This type is not supported for a custom UI Automation property. |
| `UIAutomationType_RectArray` An array of [RECT](/en-us/windows/desktop/api/windef/ns-windef-rect) structures, each containing the coordinates of the upper-left and lower-right corners of a rectangle. This type is not supported for a custom UI Automation property. |
| `UIAutomationType_ElementArray` An array of pointers to [IUIAutomationElement](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationelement) interfaces, each for a UI Automation element. |
| `UIAutomationType_OutInt` The address of a variable that receives an integer value. |
| `UIAutomationType_OutBool` The address of a variable that receives a Boolean value. |
| `UIAutomationType_OutString` The address of a variable that receives a null-terminated character string. |
| `UIAutomationType_OutDouble` The address of a variable that receives a double-precision floating-point number. |
| `UIAutomationType_OutPoint` The address of a variable that receives a [POINT](/en-us/windows/win32/api/windef/ns-windef-point) structure. |
| `UIAutomationType_OutRect` The address of a variable that receives a [RECT](/en-us/windows/desktop/api/windef/ns-windef-rect) structure. |
| `UIAutomationType_OutElement` The address of a variable that receives a pointer to the [IUIAutomationElement](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationelement) interface of a UI Automation element. |
| `UIAutomationType_OutIntArray` The address of a variable that receives an array of integer values. |
| `UIAutomationType_OutBoolArray` The address of a variable that receives an array of Boolean values. |
| `UIAutomationType_OutStringArray` The address of a variable that receives an array of null-terminated character strings. |
| `UIAutomationType_OutDoubleArray` The address of a variable that receives an array of double-precision floating-point numbers. |
| `UIAutomationType_OutPointArray` The address of a variable that receives an array of [POINT](/en-us/windows/win32/api/windef/ns-windef-point) structures. |
| `UIAutomationType_OutRectArray` The address of a variable that receives an array of [RECT](/en-us/windows/desktop/api/windef/ns-windef-rect) structures. |
| `UIAutomationType_OutElementArray` The address of a variable that receives an array of pointers to the [IUIAutomationElement](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationelement) interfaces of UI Automation elements. |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps | UWP apps] |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

---
