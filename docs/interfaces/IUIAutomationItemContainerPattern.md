# IUIAutomationItemContainerPattern

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nn-uiautomationclient-iuiautomationitemcontainerpattern)

# IUIAutomationItemContainerPattern interface (uiautomationclient.h)

Exposes a method that retrieves an item from a container, such as a virtual list.

## Inheritance

The **IUIAutomationItemContainerPattern** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **IUIAutomationItemContainerPattern** also has these types of members:

## Methods

The **IUIAutomationItemContainerPattern** interface has these methods.

|  |
| --- |
| [IUIAutomationItemContainerPattern::FindItemByProperty](nf-uiautomationclient-iuiautomationitemcontainerpattern-finditembyproperty)   Retrieves an element within a containing element, based on a specified property value. (IUIAutomationItemContainerPattern.FindItemByProperty) |

## Remarks

This interface is not limited to use by virtualized containers. Any container that can implement efficient name lookup can support this *control pattern*, enabling clients to look up names more quickly than by using methods such as [FindFirst](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-findfirst), which must traverse the Microsoft UI Automation tree.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[Control Pattern Interfaces for Clients](/en-us/windows/desktop/WinAuto/uiauto-client-controlpatterninterfaces)

---
