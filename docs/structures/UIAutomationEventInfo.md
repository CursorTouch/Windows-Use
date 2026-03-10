# UIAutomationEventInfo

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/ns-uiautomationcore-uiautomationeventinfo)

# UIAutomationEventInfo structure (uiautomationcore.h)

Contains information about a custom event.

## Syntax

```
struct UIAutomationEventInfo {
  GUID    guid;
  LPCWSTR pProgrammaticName;
};
```

## Members

`guid`

Type: **GUID**

The event identifier.

`pProgrammaticName`

Type: **[LPCWSTR](/en-us/windows/desktop/WinProg/windows-data-types)**

The programmatic name of the event (a non-localizable string).

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps | UWP apps] |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[Custom Properties, Events, and Control Patterns](/en-us/windows/desktop/WinAuto/uiauto-custompropertieseventscontrolpatterns)

[RegisterEvent](/en-us/windows/desktop/api/uiautomationcore/nf-uiautomationcore-iuiautomationregistrar-registerevent)

---
