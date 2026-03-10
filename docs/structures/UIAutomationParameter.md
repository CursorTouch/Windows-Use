# UIAutomationParameter

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/ns-uiautomationcore-uiautomationparameter)

# UIAutomationParameter structure (uiautomationcore.h)

Contains information about a parameter of a custom control pattern.

## Syntax

```
struct UIAutomationParameter {
  UIAutomationType type;
  void             *pData;
};
```

## Members

`type`

Type: **[UIAutomationType](/en-us/windows/desktop/api/uiautomationcore/ne-uiautomationcore-uiautomationtype)**

A value indicating the type of the parameter.

`pData`

Type: **void\***

A pointer to the parameter data.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps | UWP apps] |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[CallMethod](/en-us/windows/desktop/api/uiautomationcore/nf-uiautomationcore-iuiautomationpatterninstance-callmethod)

[Custom Properties, Events, and Control Patterns](/en-us/windows/desktop/WinAuto/uiauto-custompropertieseventscontrolpatterns)

[Dispatch](/en-us/windows/desktop/api/uiautomationcore/nf-uiautomationcore-iuiautomationpatternhandler-dispatch)

**Reference**

---
