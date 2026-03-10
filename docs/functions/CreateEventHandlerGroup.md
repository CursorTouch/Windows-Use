# CreateEventHandlerGroup

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomation6-createeventhandlergroup)

# IUIAutomation6::CreateEventHandlerGroup method (uiautomationclient.h)

Registers one or more event listeners in a single method call.

Important

Microsoft UI Automation clients should use the handler group methods to register event listeners instead of individual event registration methods defined in the various [IUIAutomation interface](nn-uiautomationclient-iuiautomation).

## Syntax

```
HRESULT CreateEventHandlerGroup(
  [out] IUIAutomationEventHandlerGroup **handlerGroup
);
```

## Parameters

`[out] handlerGroup`

A collection of UI Automation event listeners.

## Return value

If this method succeeds, it returns S\_OK. Otherwise, it returns an HRESULT error code.

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

[AddEventHandlerGroup](nf-uiautomationclient-iuiautomation6-addeventhandlergroup), [IUIAutomation6 interface](nn-uiautomationclient-iuiautomation6), [IUIAutomation6::RemoveEventHandlerGroup](nf-uiautomationclient-iuiautomation6-removeeventhandlergroup)

---
