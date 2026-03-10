# GetWinEventsForAutomationEvent

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationproxyfactoryentry-getwineventsforautomationevent)

# IUIAutomationProxyFactoryEntry::GetWinEventsForAutomationEvent method (uiautomationclient.h)

Retrieves the list of WinEvents that are mapped to a specific Microsoft UI Automation event. If an element represented by this proxy raises one the listed WinEvents, the proxy handles it.

## Syntax

```
HRESULT GetWinEventsForAutomationEvent(
  [in]          EVENTID    eventId,
  [in]          PROPERTYID propertyId,
  [out, retval] SAFEARRAY  **winEvents
);
```

## Parameters

`[in] eventId`

Type: **EVENTID**

The event identifier. For a list of event identifiers, see [Event Identifiers](/en-us/windows/desktop/WinAuto/uiauto-event-ids).

`[in] propertyId`

Type: **PROPERTYID**

The property identifier. For a list of property IDs, see [Property Identifiers](/en-us/windows/desktop/WinAuto/uiauto-entry-propids).

`[out, retval] winEvents`

Type: **[SAFEARRAY](/en-us/windows/win32/api/oaidl/ns-oaidl-safearray)\*\***

Receives a pointer to the list of WinEvents that map to this event.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[Best Practices for Using Safe Arrays](/en-us/windows/desktop/WinAuto/uiauto-workingwithsafearrays)

**Conceptual**

[IUIAutomationProxyFactoryEntry](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationproxyfactoryentry)

**Reference**

[SetWinEventsForAutomationEvent](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationproxyfactoryentry-setwineventsforautomationevent)

---
