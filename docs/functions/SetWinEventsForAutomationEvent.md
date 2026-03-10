# SetWinEventsForAutomationEvent

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationproxyfactoryentry-setwineventsforautomationevent)

# IUIAutomationProxyFactoryEntry::SetWinEventsForAutomationEvent method (uiautomationclient.h)

Maps Microsoft UI Automation events to WinEvents.

## Syntax

```
HRESULT SetWinEventsForAutomationEvent(
  [in] EVENTID    eventId,
  [in] PROPERTYID propertyId,
  [in] SAFEARRAY  *winEvents
);
```

## Parameters

`[in] eventId`

Type: **EVENTID**

The event identifier. For a list of event identifiers, see [Event Identifiers](/en-us/windows/desktop/WinAuto/uiauto-event-ids).

`[in] propertyId`

Type: **PROPERTYID**

The property identifier. For a list of property IDs, see [Property Identifiers](/en-us/windows/desktop/WinAuto/uiauto-entry-propids).

`[in] winEvents`

Type: **[SAFEARRAY](/en-us/windows/win32/api/oaidl/ns-oaidl-safearray)\***

The list of WinEvents that map to this event.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

When a client application subscribes to a UI Automation event, the UI Automation core also listens for WinEvents that map to this event. For example, suppose that [UIA\_Invoke\_InvokedEventId](/en-us/windows/desktop/WinAuto/uiauto-event-ids) is mapped to [EVENT\_OBJECT\_INVOKED](/en-us/windows/desktop/WinAuto/event-constants). When **EVENT\_OBJECT\_INVOKED** is raised, the client instantiates the proxy and calls [RespondToWinEvent](/en-us/windows/desktop/api/uiautomationcore/nf-uiautomationcore-iproxyproviderwineventhandler-respondtowinevent) on that proxy. In the implementation of **RespondToWinEvent**, the proxy calls [AddAutomationEvent](/en-us/windows/desktop/api/uiautomationcore/nf-uiautomationcore-iproxyproviderwineventsink-addautomationevent). The core then raises the corresponding UI Automation event.

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

[GetWinEventsForAutomationEvent](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationproxyfactoryentry-getwineventsforautomationevent)

[IUIAutomationProxyFactoryEntry](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationproxyfactoryentry)

**Reference**

---
