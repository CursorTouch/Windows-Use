# UiaRaiseAutomationEvent

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/nf-uiautomationcoreapi-uiaraiseautomationevent)

# UiaRaiseAutomationEvent function (uiautomationcoreapi.h)

Notifies listeners of an event.

## Syntax

```
HRESULT UiaRaiseAutomationEvent(
  [in] IRawElementProviderSimple *pProvider,
  [in] EVENTID                   id
);
```

## Parameters

`[in] pProvider`

Type: **[IRawElementProviderSimple](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-irawelementprovidersimple)\***

The provider element where the event occurred.

`[in] id`

Type: **EVENTID**

The identifier of the event to be raised. For a list of event IDs, see [Event Identifiers](/en-us/windows/desktop/WinAuto/uiauto-event-ids).

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this function succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

This function increments the reference counter of the *pProvider* interface, and UI Automation decrements the reference counter when the event handers finish processing the event.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2003 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcoreapi.h |
| **Library** | Uiautomationcore.lib |
| **DLL** | Uiautomationcore.dll |

---
