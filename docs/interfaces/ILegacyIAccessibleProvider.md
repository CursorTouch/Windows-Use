# ILegacyIAccessibleProvider

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nn-uiautomationcore-ilegacyiaccessibleprovider)

# ILegacyIAccessibleProvider interface (uiautomationcore.h)

Enables Microsoft UI Automation clients to access the underlying [IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible) implementation of Microsoft Active Accessibility elements.

## Inheritance

The **ILegacyIAccessibleProvider** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **ILegacyIAccessibleProvider** also has these types of members:

## Methods

The **ILegacyIAccessibleProvider** interface has these methods.

|  |
| --- |
| [ILegacyIAccessibleProvider::DoDefaultAction](nf-uiautomationcore-ilegacyiaccessibleprovider-dodefaultaction)   Performs the default action on the control. |
| [ILegacyIAccessibleProvider::get\_ChildId](nf-uiautomationcore-ilegacyiaccessibleprovider-get_childid)   Specifies the child identifier of this element. |
| [ILegacyIAccessibleProvider::get\_DefaultAction](nf-uiautomationcore-ilegacyiaccessibleprovider-get_defaultaction)   Contains a description of the default action for this element. |
| [ILegacyIAccessibleProvider::get\_Description](nf-uiautomationcore-ilegacyiaccessibleprovider-get_description)   Contains the description of this element. |
| [ILegacyIAccessibleProvider::get\_Help](nf-uiautomationcore-ilegacyiaccessibleprovider-get_help)   Specifies a string that contains help information for this element. |
| [ILegacyIAccessibleProvider::get\_KeyboardShortcut](nf-uiautomationcore-ilegacyiaccessibleprovider-get_keyboardshortcut)   Specifies the keyboard shortcut for this element. |
| [ILegacyIAccessibleProvider::get\_Name](nf-uiautomationcore-ilegacyiaccessibleprovider-get_name)   Specifies the name of this element. |
| [ILegacyIAccessibleProvider::get\_Role](nf-uiautomationcore-ilegacyiaccessibleprovider-get_role)   Specifies the role identifier of this element. |
| [ILegacyIAccessibleProvider::get\_State](nf-uiautomationcore-ilegacyiaccessibleprovider-get_state)   Specifies the state of this element. |
| [ILegacyIAccessibleProvider::get\_Value](nf-uiautomationcore-ilegacyiaccessibleprovider-get_value)   Specifies the value of this element. |
| [ILegacyIAccessibleProvider::GetIAccessible](nf-uiautomationcore-ilegacyiaccessibleprovider-getiaccessible)   Retrieves an accessible object that corresponds to a UI Automation element that supports the LegacyIAccessible control pattern. |
| [ILegacyIAccessibleProvider::GetSelection](nf-uiautomationcore-ilegacyiaccessibleprovider-getselection)   Retrieves the selected item or items in the control. |
| [ILegacyIAccessibleProvider::Select](nf-uiautomationcore-ilegacyiaccessibleprovider-select)   Selects the element. |
| [ILegacyIAccessibleProvider::SetValue](nf-uiautomationcore-ilegacyiaccessibleprovider-setvalue)   Sets the string value of the control. |

## Remarks

This interface is implemented by the Microsoft Active Accessibility to UI Automation Proxy to expose native MSAA properties and methods to UI Automation clients that need them for legacy reasons. The proxy automatically supplies this interface for applications or controls that implement Microsoft Active Accessibility natively. This interface is not intended to be implemented by UI Automation applications or controls.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

---
