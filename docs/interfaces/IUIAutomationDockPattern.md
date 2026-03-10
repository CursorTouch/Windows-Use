# IUIAutomationDockPattern

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nn-uiautomationclient-iuiautomationdockpattern)

# IUIAutomationDockPattern interface (uiautomationclient.h)

Provides access to a control that enables child elements to be arranged horizontally and vertically, relative to each other.

## Inheritance

The **IUIAutomationDockPattern** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **IUIAutomationDockPattern** also has these types of members:

## Methods

The **IUIAutomationDockPattern** interface has these methods.

|  |
| --- |
| [IUIAutomationDockPattern::get\_CachedDockPosition](nf-uiautomationclient-iuiautomationdockpattern-get_cacheddockposition)   Retrieves the cached dock position of this element within its docking container. |
| [IUIAutomationDockPattern::get\_CurrentDockPosition](nf-uiautomationclient-iuiautomationdockpattern-get_currentdockposition)   Retrieves the dock position of this element within its docking container. |
| [IUIAutomationDockPattern::SetDockPosition](nf-uiautomationclient-iuiautomationdockpattern-setdockposition)   Sets the dock position of this element. |

## Remarks

Microsoft UI Automation client applications use this interface to access the dock properties of UI Automation elements that function as controls within a docking container. A docking container is a control that allows the arrangement of child elements, both horizontally and vertically, relative to the boundaries of the docking container and other elements within the container. Controls are docked relative to each other based on their current z-order; the higher their z-order placement the farther they are placed from the specified edge of the docking container.

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
