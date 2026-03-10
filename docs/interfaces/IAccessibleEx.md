# IAccessibleEx

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nn-uiautomationcore-iaccessibleex)

# IAccessibleEx interface (uiautomationcore.h)

Exposes methods that are called by [Microsoft UI Automation](/en-us/windows/win32/winauto/entry-uiauto-win32) to retrieve extra information about a control that supports [Microsoft Active Accessibility](/en-us/windows/win32/winauto/microsoft-active-accessibility).

## Inheritance

The **IAccessibleEx** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **IAccessibleEx** also has these types of members:

## Methods

The **IAccessibleEx** interface has these methods.

|  |
| --- |
| [IAccessibleEx::ConvertReturnedElement](nf-uiautomationcore-iaccessibleex-convertreturnedelement)   Retrieves the IAccessibleEx interface of an element returned as a property value. |
| [IAccessibleEx::GetIAccessiblePair](nf-uiautomationcore-iaccessibleex-getiaccessiblepair)   Retrieves the IAccessible interface and child ID for this item. |
| [IAccessibleEx::GetObjectForChild](nf-uiautomationcore-iaccessibleex-getobjectforchild)   Retrieves an IAccessibleEx interface representing the specified child of this element. |
| [IAccessibleEx::GetRuntimeId](nf-uiautomationcore-iaccessibleex-getruntimeid)   Retrieves the runtime identifier of this element. |

## Remarks

This interface can be implemented on custom controls that also implement the [IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible) interface, to provide added support for UI Automation without the cost of a full UI Automation provider implementation.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[Adding UI Automation Functionality to Active Accessibility Servers](/en-us/windows/desktop/WinAuto/uiauto-usingiaccessibleex)

---
