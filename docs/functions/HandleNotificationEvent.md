# HandleNotificationEvent

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationnotificationeventhandler-handlenotificationevent)

# IUIAutomationNotificationEventHandler::HandleNotificationEvent method (uiautomationclient.h)

Handles a Microsoft UI Automation notification event.

## Syntax

```
HRESULT HandleNotificationEvent(
  [in] IUIAutomationElement   *sender,
       NotificationKind       notificationKind,
       NotificationProcessing notificationProcessing,
       BSTR                   displayString,
       BSTR                   activityId
);
```

## Parameters

`[in] sender`

A pointer to the element that raised the event.

`notificationKind`

The type of notification.

`notificationProcessing`

Indicates how to process notifications.

`displayString`

A string to display in the notification message.

`activityId`

A unique non-localized string to identify an action or group of actions. This is used to pass additional information to the event handler.

## Return value

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

This method is implemented by the application to handle events that it has subscribed to by calling [AddNotificationEventHandler](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomation5-addnotificationeventhandler).

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 10, version 1709 [desktop apps only] |
| **Minimum supported server** | Windows Server 2016 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[IUIAutomationNotificationEventHandler](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationnotificationeventhandler)

---
