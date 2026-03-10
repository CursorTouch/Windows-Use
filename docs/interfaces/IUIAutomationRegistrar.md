# IUIAutomationRegistrar

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nn-uiautomationcore-iuiautomationregistrar)

# IUIAutomationRegistrar interface (uiautomationcore.h)

Exposes methods for registering new control patterns, properties, and events.

## Inheritance

The **IUIAutomationRegistrar** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **IUIAutomationRegistrar** also has these types of members:

## Methods

The **IUIAutomationRegistrar** interface has these methods.

|  |
| --- |
| [IUIAutomationRegistrar::RegisterEvent](nf-uiautomationcore-iuiautomationregistrar-registerevent)   Registers a third-party Microsoft UI Automation event. |
| [IUIAutomationRegistrar::RegisterPattern](nf-uiautomationcore-iuiautomationregistrar-registerpattern)   Registers a third-party control pattern. |
| [IUIAutomationRegistrar::RegisterProperty](nf-uiautomationcore-iuiautomationregistrar-registerproperty)   Registers a third-party property. |

## Remarks

The **IUIAutomationRegistrar** interface is exposed by the [CUIAutomationRegistrar](/en-us/previous-versions/windows/desktop/legacy/ff384837(v=vs.85)) object. To obtain an instance of this object, call the [CoCreateInstance](/en-us/windows/desktop/api/combaseapi/nf-combaseapi-cocreateinstance) function with a class ID of **CLSID\_CUIAutomationRegistrar**.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[UI Automation Element Interfaces for Clients](/en-us/windows/desktop/WinAuto/uiauto-entry-uiautoclientinterfaces)

---
