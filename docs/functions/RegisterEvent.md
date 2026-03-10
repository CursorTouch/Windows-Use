# RegisterEvent

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nf-uiautomationcore-iuiautomationregistrar-registerevent)

# IUIAutomationRegistrar::RegisterEvent method (uiautomationcore.h)

Registers a third-party Microsoft UI Automation event.

## Syntax

```
HRESULT RegisterEvent(
  [in]  const UIAutomationEventInfo *event,
  [out] EVENTID                     *eventId
);
```

## Parameters

`[in] event`

Type: **[UIAutomationEventInfo](/en-us/windows/desktop/api/uiautomationcore/ns-uiautomationcore-uiautomationeventinfo)**\*

A pointer to a structure that contains information about the event to register.

`[out] eventId`

Type: **EVENTID**\*

Receives the event identifier. For a list of event IDs, see [Event Identifiers](/en-us/windows/desktop/WinAuto/uiauto-event-ids).

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

The event ID can be used in various event methods, and as a WinEvent value for events in [IAccessibleEx](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-iaccessibleex) implementations.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[IUIAutomationRegistrar](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-iuiautomationregistrar)

---
