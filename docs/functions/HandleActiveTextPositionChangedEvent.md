# HandleActiveTextPositionChangedEvent

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationactivetextpositionchangedeventhandler-handleactivetextpositionchangedevent)

# IUIAutomationActiveTextPositionChangedEventHandler::HandleActiveTextPositionChangedEvent method (uiautomationclient.h)

Handles a Microsoft UI Automation active text position change event.

**Note**  This method is implemented by the application to handle events that it has subscribed to by calling [AddActiveTextPositionChangedEventHandler](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomation6-addactivetextpositionchangedeventhandler).

## Syntax

```
HRESULT HandleActiveTextPositionChangedEvent(
  [in] IUIAutomationElement   *sender,
       IUIAutomationTextRange *range
);
```

## Parameters

`[in] sender`

A pointer to the UI Automation element that raised the event.

`range`

A span of continuous text in a container that supports the [IUIAutomationTextPattern](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationtextpattern) interface.

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
| **DLL** | UIAutomationCore.dll |

## See also

[IUIAutomationActiveTextPositionChangedEventHandler](nn-uiautomationclient-iuiautomationactivetextpositionchangedeventhandler)

---
