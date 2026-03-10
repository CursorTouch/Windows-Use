# IUIAutomation6

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nn-uiautomationclient-iuiautomation6)

# IUIAutomation6 interface (uiautomationclient.h)

Extends the [IUIAutomation5](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomation5) interface to expose additional methods for controlling Microsoft UI Automation functionality.

## Inheritance

The **IUIAutomation6** interface inherits from [IUIAutomation5](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomation5). **IUIAutomation6** also has these types of members:

## Methods

The **IUIAutomation6** interface has these methods.

|  |
| --- |
| [IUIAutomation6::AddActiveTextPositionChangedEventHandler](nf-uiautomationclient-iuiautomation6-addactivetextpositionchangedeventhandler)   Registers a method that handles when the active text position changes. |
| [IUIAutomation6::AddEventHandlerGroup](nf-uiautomationclient-iuiautomation6-addeventhandlergroup)   Registers a collection of event handler methods specified with the CreateEventHandlerGroup. |
| [IUIAutomation6::CreateEventHandlerGroup](nf-uiautomationclient-iuiautomation6-createeventhandlergroup)   Registers one or more event listeners in a single method call. |
| [IUIAutomation6::get\_CoalesceEvents](nf-uiautomationclient-iuiautomation6-get_coalesceevents)   Gets or sets whether an accessible technology client receives all events, or a subset where duplicate events are detected and filtered. (Get) |
| [IUIAutomation6::get\_ConnectionRecoveryBehavior](nf-uiautomationclient-iuiautomation6-get_connectionrecoverybehavior)   Indicates whether an accessible technology client adjusts provider request timeouts when the provider is non-responsive. (Get) |
| [IUIAutomation6::put\_CoalesceEvents](nf-uiautomationclient-iuiautomation6-put_coalesceevents)   Gets or sets whether an accessible technology client receives all events, or a subset where duplicate events are detected and filtered. (Put) |
| [IUIAutomation6::put\_ConnectionRecoveryBehavior](nf-uiautomationclient-iuiautomation6-put_connectionrecoverybehavior)   Indicates whether an accessible technology client adjusts provider request timeouts when the provider is non-responsive. (Put) |
| [IUIAutomation6::RemoveActiveTextPositionChangedEventHandler](nf-uiautomationclient-iuiautomation6-removeactivetextpositionchangedeventhandler)   Removes an active text position changed event handler. |
| [IUIAutomation6::RemoveEventHandlerGroup](nf-uiautomationclient-iuiautomation6-removeeventhandlergroup)   Asynchronously removes the specified UI Automation event handler group. |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 10, version 1809 [desktop apps only] |
| **Minimum supported server** | Windows Server, version 1709 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[IUIAutomation5](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomation5)

[UI Automation Element Interfaces for Clients](/en-us/windows/desktop/WinAuto/uiauto-entry-uiautoclientinterfaces)

---
