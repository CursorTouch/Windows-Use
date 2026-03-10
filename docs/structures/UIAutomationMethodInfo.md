# UIAutomationMethodInfo

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/ns-uiautomationcore-uiautomationmethodinfo)

# UIAutomationMethodInfo structure (uiautomationcore.h)

Contains information about a method that is supported by a custom control pattern.

## Syntax

```
struct UIAutomationMethodInfo {
  LPCWSTR          pProgrammaticName;
  BOOL             doSetFocus;
  UINT             cInParameters;
  UINT             cOutParameters;
  UIAutomationType *pParameterTypes;
  LPCWSTR          *pParameterNames;
};
```

## Members

`pProgrammaticName`

Type: **[LPCWSTR](/en-us/windows/desktop/WinProg/windows-data-types)**

The name of the method (a non-localizable string).

`doSetFocus`

Type: **[BOOL](/en-us/windows/desktop/WinProg/windows-data-types)**

**TRUE** if UI Automation should set the focus on the object before calling the method; otherwise **FALSE**.

`cInParameters`

Type: **[UINT](/en-us/windows/desktop/WinProg/windows-data-types)**

The count of [in] parameters, which are always first in the **pParameterTypes** array.

`cOutParameters`

Type: **[UINT](/en-us/windows/desktop/WinProg/windows-data-types)**

The count of [out] parameters, which always follow the [in] parameters in the **pParameterTypes** array.

`pParameterTypes`

Type: **[UIAutomationType](/en-us/windows/desktop/api/uiautomationcore/ne-uiautomationcore-uiautomationtype)\***

A pointer to an array of values indicating the data types of the parameters of the method. The data types of the In parameters should be first, followed by those of the Out parameters.

`pParameterNames`

Type: **[LPCWSTR](/en-us/windows/desktop/WinProg/windows-data-types)\***

A pointer to an array containing the parameter names (non-localizable strings).

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[Custom Properties, Events, and Control Patterns](/en-us/windows/desktop/WinAuto/uiauto-custompropertieseventscontrolpatterns)

[UIAutomationPatternInfo](/en-us/windows/desktop/api/uiautomationcore/ns-uiautomationcore-uiautomationpatterninfo)

---
