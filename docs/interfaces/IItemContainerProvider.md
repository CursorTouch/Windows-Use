# IItemContainerProvider

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nn-uiautomationcore-iitemcontainerprovider)

# IItemContainerProvider interface (uiautomationcore.h)

Provides access to controls that act as containers of other controls, such as a virtual list-view.

## Inheritance

The **IItemContainerProvider** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **IItemContainerProvider** also has these types of members:

## Methods

The **IItemContainerProvider** interface has these methods.

|  |
| --- |
| [IItemContainerProvider::FindItemByProperty](nf-uiautomationcore-iitemcontainerprovider-finditembyproperty)   Retrieves an element within a containing element, based on a specified property value. (IItemContainerProvider.FindItemByProperty) |

## Remarks

The [ItemContainer](/en-us/windows/desktop/WinAuto/uiauto-implementingitemcontainer) control pattern allows a container object to efficiently lookup an item by a
specified automation element property, such as Name, AutomationId, or IsSelected state. While this control
pattern is introduced with a view to being used by virtualized containers, it can be implemented by any container
that provides name lookup, independently of whether that container uses virtualization.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[UI Automation Providers Overview](/en-us/windows/desktop/WinAuto/uiauto-providersoverview)

---
