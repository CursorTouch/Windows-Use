# IUIAutomationProxyFactory

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nn-uiautomationclient-iuiautomationproxyfactory)

# IUIAutomationProxyFactory interface (uiautomationclient.h)

Exposes properties and methods of an object that creates a Microsoft UI Automation provider for UI elements that do not have native support for UI Automation. This interface is implemented by proxies.

## Inheritance

The **IUIAutomationProxyFactory** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **IUIAutomationProxyFactory** also has these types of members:

## Methods

The **IUIAutomationProxyFactory** interface has these methods.

|  |
| --- |
| [IUIAutomationProxyFactory::CreateProvider](nf-uiautomationclient-iuiautomationproxyfactory-createprovider)   Creates a proxy object that provides Microsoft UI Automation support for a UI element. |
| [IUIAutomationProxyFactory::get\_ProxyFactoryId](nf-uiautomationclient-iuiautomationproxyfactory-get_proxyfactoryid)   Retrieves the identifier of the proxy factory. |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[Proxy Factory Interfaces for Clients](/en-us/windows/desktop/WinAuto/uiauto-client-proxyfactoryinterfaces)

---
