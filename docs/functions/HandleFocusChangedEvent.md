# HandleFocusChangedEvent

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationfocuschangedeventhandler-handlefocuschangedevent)

# IUIAutomationFocusChangedEventHandler::HandleFocusChangedEvent method (uiautomationclient.h)

Handles the event raised when the keyboard focus moves to a different UI Automation element.

## Syntax

```
HRESULT HandleFocusChangedEvent(
  [in] IUIAutomationElement *sender
);
```

## Parameters

`[in] sender`

Type: **[IUIAutomationElement](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationelement)\***

A pointer to the element that has received the focus.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

This method is implemented by the application to handle events that were subscribed to by using [AddFocusChangedEventHandler](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomation-addfocuschangedeventhandler)

The UI Automation element represented by *sender* might not have any cached properties or control patterns, depending on whether the application subscribed to this event while a cache request was active.

Adjusting an event handler from within this method is not supported.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[IUIAutomationFocusChangedEventHandler](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationfocuschangedeventhandler)

---
