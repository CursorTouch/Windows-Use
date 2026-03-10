# UiaRaiseNotificationEvent

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/nf-uiautomationcoreapi-uiaraisenotificationevent)

# UiaRaiseNotificationEvent function (uiautomationcoreapi.h)

Called by providers to initiate a notification event.

## Syntax

```
HRESULT UiaRaiseNotificationEvent(
  [in]           IRawElementProviderSimple *provider,
                 NotificationKind          notificationKind,
                 NotificationProcessing    notificationProcessing,
  [in, optional] BSTR                      displayString,
  [in]           BSTR                      activityId
);
```

## Parameters

`[in] provider`

The provider node where the notification event occurred.

`notificationKind`

The type of notification, as a [NotificationKind enumeration](../uiautomationcore/ne-uiautomationcore-notificationkind) value.

`notificationProcessing`

The preferred way to process a notification, as a [NotificationProcessing enumeration](../uiautomationcore/ne-uiautomationcore-notificationprocessing) value.

`[in, optional] displayString`

A string to display in the notification message.

`[in] activityId`

A unique non-localized string to identify an action or group of actions. Use this to pass additional information to the event handler.

## Return value

If this function succeeds, it returns S\_OK. Otherwise, it returns an HRESULT error code.

## Remarks

If your window uses the [`WS_POPUP`](/en-us/windows/win32/winmsg/window-styles) style, it must also implement the [Window Control Pattern](/en-us/windows/win32/winauto/uiauto-implementingwindow) and handle the [WM\_GETOBJECT](/en-us/windows/win32/winauto/wm-getobject) message (see [How to Expose a Server-Side UI Automation Provider](/en-us/windows/win32/winauto/uiauto-howto-expose-serverside-uiautomation-provider) for more details).

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 10, version 1709 [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2016 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcoreapi.h (include UIAutomation.h) |
| **Library** | Uiautomationcore.lib |
| **DLL** | Uiautomationcore.dll |

---
