# ISelectionProvider

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nn-uiautomationcore-iselectionprovider)

# ISelectionProvider interface (uiautomationcore.h)

Provides access
to controls that act as containers for a collection of individual, selectable child items.
The children of this control must implement [ISelectionItemProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-iselectionitemprovider).

## Inheritance

The **ISelectionProvider** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **ISelectionProvider** also has these types of members:

## Methods

The **ISelectionProvider** interface has these methods.

|  |
| --- |
| [ISelectionProvider::get\_CanSelectMultiple](nf-uiautomationcore-iselectionprovider-get_canselectmultiple)   Indicates whether the Microsoft UI Automation provider allows more than one child element to be selected concurrently. |
| [ISelectionProvider::get\_IsSelectionRequired](nf-uiautomationcore-iselectionprovider-get_isselectionrequired)   Indicates whether the Microsoft UI Automation provider requires at least one child element to be selected. |
| [ISelectionProvider::GetSelection](nf-uiautomationcore-iselectionprovider-getselection)   Retrieves a Microsoft UI Automation provider for each child element that is selected. |

## Remarks

This interface is implemented by a UI Automation provider.

Providers should raise an event of type [UIA\_Selection\_InvalidatedEventId](/en-us/windows/desktop/WinAuto/uiauto-event-ids) when a selection in a container has changed significantly.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2003 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[UI Automation Providers Overview](/en-us/windows/desktop/WinAuto/uiauto-providersoverview)

---
