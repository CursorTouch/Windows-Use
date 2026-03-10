# UIAutomationPropertyInfo

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/ns-uiautomationcore-uiautomationpropertyinfo)

# UIAutomationPropertyInfo structure (uiautomationcore.h)

Contains information about a custom property.

## Syntax

```
struct UIAutomationPropertyInfo {
  GUID             guid;
  LPCWSTR          pProgrammaticName;
  UIAutomationType type;
};
```

## Members

`guid`

Type: **GUID**

The unique identifier of the property.

`pProgrammaticName`

Type: **[LPCWSTR](/en-us/windows/desktop/WinProg/windows-data-types)**

The programmatic name of the property (a non-localizable string).

`type`

Type: **[UIAutomationType](/en-us/windows/desktop/api/uiautomationcore/ne-uiautomationcore-uiautomationtype)**

A value from the [UIAutomationType](/en-us/windows/desktop/api/uiautomationcore/ne-uiautomationcore-uiautomationtype) enumerated type indicating the data type of the property value.

## Remarks

A custom property must have one of the following data types specified by the [UIAutomationType](/en-us/windows/desktop/api/uiautomationcore/ne-uiautomationcore-uiautomationtype) enumeration. No other data types are supported for custom properties. For more information, see [Custom Properties, Events, and Control Patterns](/en-us/windows/desktop/WinAuto/uiauto-custompropertieseventscontrolpatterns).

* [UIAutomationType\_Bool](/en-us/windows/desktop/api/uiautomationcore/ne-uiautomationcore-uiautomationtype)
* [UIAutomationType\_Double](/en-us/windows/desktop/api/uiautomationcore/ne-uiautomationcore-uiautomationtype)
* [UIAutomationType\_Element](/en-us/windows/desktop/api/uiautomationcore/ne-uiautomationcore-uiautomationtype)
* [UIAutomationType\_Int](/en-us/windows/desktop/api/uiautomationcore/ne-uiautomationcore-uiautomationtype)
* [UIAutomationType\_Point](/en-us/windows/desktop/api/uiautomationcore/ne-uiautomationcore-uiautomationtype)
* [UIAutomationType\_String](/en-us/windows/desktop/api/uiautomationcore/ne-uiautomationcore-uiautomationtype)

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps | UWP apps] |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[Custom Properties, Events, and Control Patterns](/en-us/windows/desktop/WinAuto/uiauto-custompropertieseventscontrolpatterns)

[RegisterProperty](/en-us/windows/desktop/api/uiautomationcore/nf-uiautomationcore-iuiautomationregistrar-registerproperty)

---
