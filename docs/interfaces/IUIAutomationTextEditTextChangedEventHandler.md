# IUIAutomationTextEditTextChangedEventHandler

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nn-uiautomationclient-iuiautomationtextedittextchangedeventhandler)

# IUIAutomationTextEditTextChangedEventHandler interface (uiautomationclient.h)

Exposes a method to handle events that occur when Microsoft UI Automation reports a text-changed event from text edit controls.

## Inheritance

The **IUIAutomationTextEditTextChangedEventHandler** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **IUIAutomationTextEditTextChangedEventHandler** also has these types of members:

## Methods

The **IUIAutomationTextEditTextChangedEventHandler** interface has these methods.

|  |
| --- |
| [IUIAutomationTextEditTextChangedEventHandler::HandleTextEditTextChangedEvent](nf-uiautomationclient-iuiautomationtextedittextchangedeventhandler-handletextedittextchangedevent)   Handles an event that is raised when a Microsoft UI Automation provider for a text-edit control reports a programmatic text change. |

## Remarks

This interface is implemented by the application to handle events that it has subscribed to by using **AddTextEditTextChangedEventHandler**.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 8.1 [desktop apps only] |
| **Minimum supported server** | Windows Server 2012 R2 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[Event Handling Interfaces for Clients](/en-us/windows/desktop/WinAuto/uiauto-client-eventhandlinginterfaces)

---
