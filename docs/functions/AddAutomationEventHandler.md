# AddAutomationEventHandler

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationeventhandlergroup-addautomationeventhandler)

# IUIAutomationEventHandlerGroup::AddAutomationEventHandler method (uiautomationclient.h)

Registers a method that handles Microsoft UI Automation events.

**Important**  UI Automation clients should use the handler group methods to register event listeners instead of individual event registration methods defined in the various [IUIAutomation](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomation) namespaces.

## Syntax

```
HRESULT AddAutomationEventHandler(
  [in] EVENTID                   eventId,
  [in] TreeScope                 scope,
  [in] IUIAutomationCacheRequest *cacheRequest,
  [in] IUIAutomationEventHandler *handler
);
```

## Parameters

`[in] eventId`

The identifier of the event that the method handles. For a list of event IDs, see [Event Identifiers](/en-us/windows/desktop/WinAuto/uiauto-event-ids).

`[in] scope`

The scope of events to be handled; that is, whether they are on the element itself, or on its ancestors and descendants.

`[in] cacheRequest`

A pointer to a cache request, or **NULL** if no caching is wanted.

`[in] handler`

A pointer to the object that handles the event.

## Return value

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 10, version 1809 [desktop apps only] |
| **Minimum supported server** | Windows Server, version 1709 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[IUIAutomationEventHandlerGroup](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationeventhandlergroup)

---
