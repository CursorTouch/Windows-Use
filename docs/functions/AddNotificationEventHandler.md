# AddNotificationEventHandler

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationeventhandlergroup-addnotificationeventhandler)

# IUIAutomationEventHandlerGroup::AddNotificationEventHandler method (uiautomationclient.h)

Registers a method that handles notification events.

**Important**  Microsoft UI Automation clients should use the handler group methods to register event listeners instead of individual event registration methods defined in the various [IUIAutomation](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomation) namespaces.

## Syntax

```
HRESULT AddNotificationEventHandler(
  [in] TreeScope                             scope,
  [in] IUIAutomationCacheRequest             *cacheRequest,
  [in] IUIAutomationNotificationEventHandler *handler
);
```

## Parameters

`[in] scope`

The scope of events to be handled; that is, whether they are on the element itself, or on its ancestors and descendants.

`[in] cacheRequest`

A pointer to a cache request, or **NULL** if no caching is wanted.

`[in] handler`

A pointer to the object that handles the notification event.

## Return value

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

Before implementing an event handler, you should be familiar with the threading issues described in [Understanding Threading Issues](/en-us/windows/desktop/WinAuto/uiauto-threading).

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
