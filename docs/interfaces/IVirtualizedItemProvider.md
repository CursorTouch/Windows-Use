# IVirtualizedItemProvider

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nn-uiautomationcore-ivirtualizeditemprovider)

# IVirtualizedItemProvider interface (uiautomationcore.h)

Provides access to virtualized items, which are items that are represented by placeholder automation elements in the Microsoft UI Automation tree.

## Inheritance

The **IVirtualizedItemProvider** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **IVirtualizedItemProvider** also has these types of members:

## Methods

The **IVirtualizedItemProvider** interface has these methods.

|  |
| --- |
| [IVirtualizedItemProvider::Realize](nf-uiautomationcore-ivirtualizeditemprovider-realize)   Makes the virtual item fully accessible as a UI Automation element. (IVirtualizedItemProvider.Realize) |

## Remarks

A virtualized item is typically an item in a virtual list; that is, a list that does not manage its own data. When an application retrieves an [IUIAutomationElement](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationelement) for a virtualized item by using [FindItemByProperty](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationitemcontainerpattern-finditembyproperty), UI Automation calls the provider's implementation of [FindItemByProperty](/en-us/windows/desktop/api/uiautomationcore/nf-uiautomationcore-iitemcontainerprovider-finditembyproperty), where the provider may return a placeholder element that also implements **IVirtualizedItemProvider**. On a call to [Realize](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationvirtualizeditempattern-realize), the provider's implementation of [Realize](/en-us/windows/desktop/api/uiautomationcore/nf-uiautomationcore-ivirtualizeditemprovider-realize) returns a full UI Automation element reference and may also scroll the item into view.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

**Conceptual**

[VirtualizedItem Control Pattern](/en-us/windows/desktop/WinAuto/uiauto-implementingvirtualizeditem)

[Working with Virtualized Items](/en-us/windows/desktop/WinAuto/uiauto-workingwithvirtualizeditems)

---
