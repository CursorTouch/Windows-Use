# IDockProvider

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nn-uiautomationcore-idockprovider)

# IDockProvider interface (uiautomationcore.h)

Provides access
to an element in a docking container.

## Inheritance

The **IDockProvider** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **IDockProvider** also has these types of members:

## Methods

The **IDockProvider** interface has these methods.

|  |
| --- |
| [IDockProvider::get\_DockPosition](nf-uiautomationcore-idockprovider-get_dockposition)   Indicates the current docking position of this element. |
| [IDockProvider::SetDockPosition](nf-uiautomationcore-idockprovider-setdockposition)   Sets the docking position of this element. |

## Remarks

**IDockProvider** does not expose any properties of the docking
container or any properties of controls that might be docked adjacent to the current
control in the docking container.

Controls are docked relative to each other based on their current z-order;
the higher their z-order placement, the farther they are placed from the specified edge of the docking container.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2003 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

**Conceptual**

[Dock Control Pattern](/en-us/windows/desktop/WinAuto/uiauto-implementingdock)

[DockPosition](/en-us/windows/desktop/api/uiautomationcore/ne-uiautomationcore-dockposition)

**Reference**

[UI Automation Providers Overview](/en-us/windows/desktop/WinAuto/uiauto-providersoverview)

---
