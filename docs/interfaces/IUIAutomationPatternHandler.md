# IUIAutomationPatternHandler

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nn-uiautomationcore-iuiautomationpatternhandler)

# IUIAutomationPatternHandler interface (uiautomationcore.h)

Returns a client API wrapper object and to unmarshal property and method requests to an actual provider instance. The PatternHandler object is stateless, so this can be implemented by a singleton.

## Inheritance

The **IUIAutomationPatternHandler** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **IUIAutomationPatternHandler** also has these types of members:

## Methods

The **IUIAutomationPatternHandler** interface has these methods.

|  |
| --- |
| [IUIAutomationPatternHandler::CreateClientWrapper](nf-uiautomationcore-iuiautomationpatternhandler-createclientwrapper)   Creates an object that enables a client application to interact with a custom control pattern. |
| [IUIAutomationPatternHandler::Dispatch](nf-uiautomationcore-iuiautomationpatternhandler-dispatch)   Dispatches a method or property getter to a custom control pattern provider. |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[Control Pattern Interfaces for Clients](/en-us/windows/desktop/WinAuto/uiauto-client-controlpatterninterfaces)

---
