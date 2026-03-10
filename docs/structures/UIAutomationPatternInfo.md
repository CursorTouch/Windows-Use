# UIAutomationPatternInfo

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/ns-uiautomationcore-uiautomationpatterninfo)

# UIAutomationPatternInfo structure (uiautomationcore.h)

Contains information about a custom control pattern.

## Syntax

```
struct UIAutomationPatternInfo {
  GUID                            guid;
  LPCWSTR                         pProgrammaticName;
  GUID                            providerInterfaceId;
  GUID                            clientInterfaceId;
  UINT                            cProperties;
  struct UIAutomationPropertyInfo *pProperties;
  UINT                            cMethods;
  struct UIAutomationMethodInfo   *pMethods;
  UINT                            cEvents;
  struct UIAutomationEventInfo    *pEvents;
  IUIAutomationPatternHandler     *pPatternHandler;
};
```

## Members

`guid`

Type: **GUID**

The unique identifier of the control pattern.

`pProgrammaticName`

Type: **[LPCWSTR](/en-us/windows/desktop/WinProg/windows-data-types)**

The name of the control pattern (a non-localizable string).

`providerInterfaceId`

Type: **GUID**

The unique identifier of the provider interface for the control pattern.

`clientInterfaceId`

Type: **GUID**

The unique identifier of the client interface for the control pattern.

`cProperties`

Type: **[UINT](/en-us/windows/desktop/WinProg/windows-data-types)**

The count of elements in **pProperties**.

`pProperties`

Type: **[UIAutomationPropertyInfo](/en-us/windows/desktop/api/uiautomationcore/ns-uiautomationcore-uiautomationpropertyinfo)\***

A pointer to an array of structures describing properties available on the control pattern.

`cMethods`

Type: **[UINT](/en-us/windows/desktop/WinProg/windows-data-types)**

The count of elements in **pMethods**.

`pMethods`

Type: **[UIAutomationMethodInfo](/en-us/windows/desktop/api/uiautomationcore/ns-uiautomationcore-uiautomationmethodinfo)\***

A pointer to an array of structures describing methods available on the control pattern.

`cEvents`

Type: **[UINT](/en-us/windows/desktop/WinProg/windows-data-types)**

The count of elements in **pEvents**.

`pEvents`

Type: **[UIAutomationEventInfo](/en-us/windows/desktop/api/uiautomationcore/ns-uiautomationcore-uiautomationeventinfo)\***

A pointer to an array of structures describing events available on the control pattern.

`pPatternHandler`

Type: **[IUIAutomationPatternHandler](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-iuiautomationpatternhandler)\***

A pointer to the object that makes the control pattern available to clients.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps | UWP apps] |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[Custom Properties, Events, and Control Patterns](/en-us/windows/desktop/WinAuto/uiauto-custompropertieseventscontrolpatterns)

[RegisterPattern](/en-us/windows/desktop/api/uiautomationcore/nf-uiautomationcore-iuiautomationregistrar-registerpattern)

---
