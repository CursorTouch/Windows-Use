# IRawElementProviderAdviseEvents

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nn-uiautomationcore-irawelementprovideradviseevents)

# IRawElementProviderAdviseEvents interface (uiautomationcore.h)

Exposes methods that are called to notify the root element of a fragment
when a Microsoft UI Automation client application begins or ends listening for events on that fragment.

## Inheritance

The **IRawElementProviderAdviseEvents** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **IRawElementProviderAdviseEvents** also has these types of members:

## Methods

The **IRawElementProviderAdviseEvents** interface has these methods.

|  |
| --- |
| [IRawElementProviderAdviseEvents::AdviseEventAdded](nf-uiautomationcore-irawelementprovideradviseevents-adviseeventadded)   Notifies the Microsoft UI Automation provider when a UI Automation client begins listening for a specific event, including a property-changed event. |
| [IRawElementProviderAdviseEvents::AdviseEventRemoved](nf-uiautomationcore-irawelementprovideradviseevents-adviseeventremoved)   Notifies the Microsoft UI Automation provider when a UI Automation client stops listening for a specific event, including a property-changed event. |

## Remarks

Implementation of this interface is optional. It can be used to improve performance by raising events only when they are being listened for.

Similar to implementing reference counting in Component Object Model (COM) programming, it is important for UI Automation providers to treat the [AdviseEventAdded](/en-us/windows/desktop/api/uiautomationcore/nf-uiautomationcore-irawelementprovideradviseevents-adviseeventadded) and [AdviseEventRemoved](/en-us/windows/desktop/api/uiautomationcore/nf-uiautomationcore-irawelementprovideradviseevents-adviseeventremoved) methods like the [AddRef](/en-us/windows/desktop/api/unknwn/nf-unknwn-iunknown-addref) and [Release](/en-us/windows/desktop/api/unknwn/nf-unknwn-iunknown-release) methods of the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface.
As long as **AdviseEventAdded** has been called more times than **AdviseEventRemoved** for a specific event or property, the provider should continue to raise corresponding events, because some clients are still listening. Alternatively, UI Automation providers can use the [UiaClientsAreListening](/en-us/windows/desktop/api/uiautomationcoreapi/nf-uiautomationcoreapi-uiaclientsarelistening) function to determine if at least one client is listening and, if so, raise all appropriate events.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2003 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

---
