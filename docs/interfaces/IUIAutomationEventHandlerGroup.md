# IUIAutomationEventHandlerGroup

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nn-uiautomationclient-iuiautomationeventhandlergroup)

# IUIAutomationEventHandlerGroup interface (uiautomationclient.h)

Exposes methods for adding one or more events to a collection for bulk registration through the [CreateEventHandlerGroup](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomation6-createeventhandlergroup) and [AddEventHandlerGroup](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomation6-addeventhandlergroup) methods defined in [IUIAutomation6](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomation6).

**Important**  Microsoft UI Automation clients should use the handler group methods to register event listeners instead of individual event registration methods defined in the various [IUIAutomation](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomation) namespaces.

## Inheritance

The **IUIAutomationEventHandlerGroup** interface inherits from the IUnknown interface.

## Methods

The **IUIAutomationEventHandlerGroup** interface has these methods.

|  |
| --- |
| [IUIAutomationEventHandlerGroup::AddActiveTextPositionChangedEventHandler](nf-uiautomationclient-iuiautomationeventhandlergroup-addactivetextpositionchangedeventhandler)   Registers a method (in an event handler group) that handles when the active text position changes. |
| [IUIAutomationEventHandlerGroup::AddAutomationEventHandler](nf-uiautomationclient-iuiautomationeventhandlergroup-addautomationeventhandler)   Registers a method that handles Microsoft UI Automation events. |
| [IUIAutomationEventHandlerGroup::AddChangesEventHandler](nf-uiautomationclient-iuiautomationeventhandlergroup-addchangeseventhandler)   Registers a method that handles change events. |
| [IUIAutomationEventHandlerGroup::AddNotificationEventHandler](nf-uiautomationclient-iuiautomationeventhandlergroup-addnotificationeventhandler)   Registers a method that handles notification events. |
| [IUIAutomationEventHandlerGroup::AddPropertyChangedEventHandler](nf-uiautomationclient-iuiautomationeventhandlergroup-addpropertychangedeventhandler)   Registers a method that handles a property-changed event. |
| [IUIAutomationEventHandlerGroup::AddStructureChangedEventHandler](nf-uiautomationclient-iuiautomationeventhandlergroup-addstructurechangedeventhandler)   Registers a method that handles structure-changed events. |
| [IUIAutomationEventHandlerGroup::AddTextEditTextChangedEventHandler](nf-uiautomationclient-iuiautomationeventhandlergroup-addtextedittextchangedeventhandler)   Registers a method that handles programmatic text-edit events. |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 10, version 1809 [desktop apps only] |
| **Minimum supported server** | Windows Server, version 1709 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[UI Automation Element Interfaces for Clients](/en-us/windows/desktop/WinAuto/uiauto-entry-uiautoclientinterfaces)

---
