# AddEventHandlerGroup

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomation6-addeventhandlergroup)

# IUIAutomation6::AddEventHandlerGroup method (uiautomationclient.h)

Registers a collection of event handler methods specified with the [IUIAutomation6::CreateEventHandlerGroup](nf-uiautomationclient-iuiautomation6-createeventhandlergroup).

Important

Microsoft UI Automation clients should use the handler group methods to register event listeners instead of individual event registration methods defined in the various [IUIAutomation interface](nn-uiautomationclient-iuiautomation) namespaces.

## Syntax

```
HRESULT AddEventHandlerGroup(
  [in] IUIAutomationElement           *element,
       IUIAutomationEventHandlerGroup *handlerGroup
);
```

## Parameters

`[in] element`

A pointer to the UI Automation element associated with the event handler group.

`handlerGroup`

A collection of UI Automation event listeners.

## Return value

If this method succeeds, it returns S\_OK. Otherwise, it returns an HRESULT error code.

## Remarks

Before implementing an event handler, you should be familiar with the threading issues described in [Understanding Threading Issues](/en-us/windows/desktop/WinAuto/uiauto-threading).

It is possible for an event to be delivered to an event handler after the handler has been unsubscribed, if the event is received simultaneously with the request to unsubscribe the event. The best practice is to follow the Component Object Model (COM) standard and avoid destroying the event handler object until its reference count has reached zero. Destroying an event handler immediately after unsubscribing for events may result in an access violation if an event is delivered late.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 10, version 1809 [desktop apps only] |
| **Minimum supported server** | Windows Server, version 1709 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[IUIAutomation6::RemoveEventHandlerGroup](nf-uiautomationclient-iuiautomation6-removeeventhandlergroup), [IUIAutomation6 interface](nn-uiautomationclient-iuiautomation6)

---
