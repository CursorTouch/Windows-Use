# RemoveFocusChangedEventHandler

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomation-removefocuschangedeventhandler)

# IUIAutomation::RemoveFocusChangedEventHandler method (uiautomationclient.h)

Removes a focus-changed event handler.

## Syntax

```
HRESULT RemoveFocusChangedEventHandler(
  [in] IUIAutomationFocusChangedEventHandler *handler
);
```

## Parameters

`[in] handler`

Type: **[IUIAutomationFocusChangedEventHandler](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationfocuschangedeventhandler)\***

A pointer to the event handler that was passed to [IUIAutomation::AddFocusChangedEventHandler](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomation-addfocuschangedeventhandler).

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

A UI Automation client should not use multiple threads to add or remove event handlers. Unexpected behavior can result if one event handler is being added or removed while another is being added or removed in the same client process.

It is possible for an event to be delivered to an event handler after the handler has been unsubscribed,
if the event is received simultaneously with the request to unsubscribe the event. The best practice
is to follow the Component Object Model (COM) standard and avoid destroying the event handler object until its reference count
has reached zero. Destroying an event handler immediately after unsubscribing for events may result in an
access violation if an event is delivered late.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[IUIAutomation](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomation)

[RemoveAllEventHandlers](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomation-removealleventhandlers)

[RemoveAutomationEventHandler](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomation-removeautomationeventhandler)

[RemovePropertyChangedEventHandler](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomation-removepropertychangedeventhandler)

[RemoveStructureChangedEventHandler](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomation-removestructurechangedeventhandler)

---
