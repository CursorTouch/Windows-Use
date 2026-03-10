# IUIAutomationVirtualizedItemPattern

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nn-uiautomationclient-iuiautomationvirtualizeditempattern)

# IUIAutomationVirtualizedItemPattern interface (uiautomationclient.h)

Represents a virtualized item, which is an item that is represented by a placeholder automation element in the Microsoft UI Automation tree.

## Inheritance

The **IUIAutomationVirtualizedItemPattern** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **IUIAutomationVirtualizedItemPattern** also has these types of members:

## Methods

The **IUIAutomationVirtualizedItemPattern** interface has these methods.

|  |
| --- |
| [IUIAutomationVirtualizedItemPattern::Realize](nf-uiautomationclient-iuiautomationvirtualizeditempattern-realize)   Creates a full UI Automation element for a virtualized item. |

## Remarks

A virtualized item can be an item retrieved from a control that supports the [ItemContainer](/en-us/windows/desktop/WinAuto/uiauto-implementingitemcontainer) control pattern, or a virtualized embedded object retrieved from a control that supports the [Text](/en-us/windows/desktop/WinAuto/uiauto-about-text-and-textrange-patterns) control pattern.

The placeholder automation element for a virtualized item might not have loaded data for all UI Automation properties, and may return [UIA\_E\_ELEMENTNOTAVAILABLE](/en-us/windows/desktop/WinAuto/uiauto-error-codes) in response to queries for properties that are not available.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[Control Pattern Interfaces for Clients](/en-us/windows/desktop/WinAuto/uiauto-client-controlpatterninterfaces)

[Working with Virtualized Items](/en-us/windows/desktop/WinAuto/uiauto-workingwithvirtualizeditems)

---
