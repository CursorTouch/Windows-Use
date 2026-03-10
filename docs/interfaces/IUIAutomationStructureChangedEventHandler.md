# IUIAutomationStructureChangedEventHandler

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nn-uiautomationclient-iuiautomationstructurechangedeventhandler)

# IUIAutomationStructureChangedEventHandler interface (uiautomationclient.h)

Exposes a method to handle events that occur when the Microsoft UI Automation tree structure is changed.

## Inheritance

The **IUIAutomationStructureChangedEventHandler** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **IUIAutomationStructureChangedEventHandler** also has these types of members:

## Methods

The **IUIAutomationStructureChangedEventHandler** interface has these methods.

|  |
| --- |
| [IUIAutomationStructureChangedEventHandler::HandleStructureChangedEvent](nf-uiautomationclient-iuiautomationstructurechangedeventhandler-handlestructurechangedevent)   Handles an event that is raised when the Microsoft UI Automation tree structure has changed. |

## Remarks

This interface is implemented by the application to handle events that it has subscribed to by using [AddStructureChangedEventHandler](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomation-addstructurechangedeventhandler).

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[Event Handling Interfaces for Clients](/en-us/windows/desktop/WinAuto/uiauto-client-eventhandlinginterfaces)

---
