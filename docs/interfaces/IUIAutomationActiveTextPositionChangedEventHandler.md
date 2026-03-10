# IUIAutomationActiveTextPositionChangedEventHandler

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nn-uiautomationclient-iuiautomationactivetextpositionchangedeventhandler)

# IUIAutomationActiveTextPositionChangedEventHandler interface (uiautomationclient.h)

Exposes a method to handle Microsoft UI Automation events that occur when the active text position changes.

**Note**  This interface is implemented by the application to handle events that it has subscribed to by calling [AddActiveTextPositionChangedEventHandler](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomation6-addactivetextpositionchangedeventhandler).

## Inheritance

The **IUIAutomationActiveTextPositionChangedEventHandler** interface inherits from the IUnknown interface.

## Methods

The **IUIAutomationActiveTextPositionChangedEventHandler** interface has these methods.

|  |
| --- |
| [IUIAutomationActiveTextPositionChangedEventHandler::HandleActiveTextPositionChangedEvent](nf-uiautomationclient-iuiautomationactivetextpositionchangedeventhandler-handleactivetextpositionchangedevent)   Handles a Microsoft UI Automation active text position change event. |

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

[Event Handling Interfaces for Clients](/en-us/windows/desktop/WinAuto/uiauto-client-eventhandlinginterfaces)

---
