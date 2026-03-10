# RemoveNotificationEventHandler

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomation5-removenotificationeventhandler)

# IUIAutomation5::RemoveNotificationEventHandler method (uiautomationclient.h)

Removes a notification event handler.

## Syntax

```
HRESULT RemoveNotificationEventHandler(
  [in] IUIAutomationElement                  *element,
  [in] IUIAutomationNotificationEventHandler *handler
);
```

## Parameters

`[in] element`

Type: **[IUIAutomationElement](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationelement)\***

A pointer to the UI Automation element from which to remove the handler.

`[in] handler`

Type: **[IUIAutomationNotificationEventHandler](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationnotificationeventhandler)\***

A pointer to the interface that was passed to [AddNotificationEventHandler](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomation5-addnotificationeventhandler).

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 10, version 1709 [desktop apps only] |
| **Minimum supported server** | Windows Server, version 1709 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[IUIAutomation5](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomation5)

[RemoveAllEventHandlers](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomation-removealleventhandlers)

---
