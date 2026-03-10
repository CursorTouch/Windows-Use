# IUIAutomationChangesEventHandler

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nn-uiautomationclient-iuiautomationchangeseventhandler)

# IUIAutomationChangesEventHandler interface (uiautomationclient.h)

Exposes a method to handle one or more Microsoft UI Automation change events.

## Inheritance

The **IUIAutomationChangesEventHandler** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **IUIAutomationChangesEventHandler** also has these types of members:

## Methods

The **IUIAutomationChangesEventHandler** interface has these methods.

|  |
| --- |
| [IUIAutomationChangesEventHandler::HandleChangesEvent](nf-uiautomationclient-iuiautomationchangeseventhandler-handlechangesevent)   Handles one or more Microsoft UI Automation change events. |

## Remarks

This interface is implemented by the application to handle events that it has subscribed to by calling [AddChangesEventHandler](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomation4-addchangeseventhandler).

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 10, version 1703 [desktop apps only] |
| **Minimum supported server** | Windows Server 2016 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[Event Handling Interfaces for Clients](/en-us/windows/desktop/WinAuto/uiauto-client-eventhandlinginterfaces)

---
