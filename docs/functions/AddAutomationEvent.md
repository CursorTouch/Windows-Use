# AddAutomationEvent

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nf-uiautomationcore-iproxyproviderwineventsink-addautomationevent)

# IProxyProviderWinEventSink::AddAutomationEvent method (uiautomationcore.h)

Raises a Microsoft UI Automation event.

## Syntax

```
HRESULT AddAutomationEvent(
  [in] IRawElementProviderSimple *pProvider,
  [in] EVENTID                   id
);
```

## Parameters

`[in] pProvider`

Type: **[IRawElementProviderSimple](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-irawelementprovidersimple)\***

A pointer to the provider for the element that will raise the event.

`[in] id`

Type: **EVENTID**

The identifier of the event that will be raised. For a list of event identifiers, see [Event Identifiers](/en-us/windows/desktop/WinAuto/uiauto-event-ids)

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[IProxyProviderWinEventSink](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-iproxyproviderwineventsink)

---
