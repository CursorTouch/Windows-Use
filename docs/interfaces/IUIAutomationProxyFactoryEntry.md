# IUIAutomationProxyFactoryEntry

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nn-uiautomationclient-iuiautomationproxyfactoryentry)

# IUIAutomationProxyFactoryEntry interface (uiautomationclient.h)

Represents a proxy factory in the table maintained by Microsoft UI Automation, and exposes properties and methods that can be used by client applications to interact with [IUIAutomationProxyFactory](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationproxyfactory) objects.

## Inheritance

The **IUIAutomationProxyFactoryEntry** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **IUIAutomationProxyFactoryEntry** also has these types of members:

## Methods

The **IUIAutomationProxyFactoryEntry** interface has these methods.

|  |
| --- |
| [IUIAutomationProxyFactoryEntry::get\_AllowSubstringMatch](nf-uiautomationclient-iuiautomationproxyfactoryentry-get_allowsubstringmatch)   Sets or retrieves a value that specifies whether the proxy allows substring matching. (Get) |
| [IUIAutomationProxyFactoryEntry::get\_CanCheckBaseClass](nf-uiautomationclient-iuiautomationproxyfactoryentry-get_cancheckbaseclass)   Sets or retrieves a value that specifies whether the base class can be checked when searching for a proxy factory. (Get) |
| [IUIAutomationProxyFactoryEntry::get\_ClassName](nf-uiautomationclient-iuiautomationproxyfactoryentry-get_classname)   Sets or retrieves the name of the window class served by the proxy factory. (Get) |
| [IUIAutomationProxyFactoryEntry::get\_ImageName](nf-uiautomationclient-iuiautomationproxyfactoryentry-get_imagename)   Sets or retrieves the name of the image of the proxy factory. (Get) |
| [IUIAutomationProxyFactoryEntry::get\_NeedsAdviseEvents](nf-uiautomationclient-iuiautomationproxyfactoryentry-get_needsadviseevents)   Sets or retrieves a value that specifies whether the proxy must be notified when an application has registered for events. (Get) |
| [IUIAutomationProxyFactoryEntry::get\_ProxyFactory](nf-uiautomationclient-iuiautomationproxyfactoryentry-get_proxyfactory)   Retrieves the proxy factory associated with this entry. |
| [IUIAutomationProxyFactoryEntry::GetWinEventsForAutomationEvent](nf-uiautomationclient-iuiautomationproxyfactoryentry-getwineventsforautomationevent)   Retrieves the list of WinEvents that are mapped to a specific Microsoft UI Automation event. If an element represented by this proxy raises one the listed WinEvents, the proxy handles it. |
| [IUIAutomationProxyFactoryEntry::put\_AllowSubstringMatch](nf-uiautomationclient-iuiautomationproxyfactoryentry-put_allowsubstringmatch)   Sets or retrieves a value that specifies whether the proxy allows substring matching. (Put) |
| [IUIAutomationProxyFactoryEntry::put\_CanCheckBaseClass](nf-uiautomationclient-iuiautomationproxyfactoryentry-put_cancheckbaseclass)   Sets or retrieves a value that specifies whether the base class can be checked when searching for a proxy factory. (Put) |
| [IUIAutomationProxyFactoryEntry::put\_ClassName](nf-uiautomationclient-iuiautomationproxyfactoryentry-put_classname)   Sets or retrieves the name of the window class served by the proxy factory. (Put) |
| [IUIAutomationProxyFactoryEntry::put\_ImageName](nf-uiautomationclient-iuiautomationproxyfactoryentry-put_imagename)   Sets or retrieves the name of the image of the proxy factory. (Put) |
| [IUIAutomationProxyFactoryEntry::put\_NeedsAdviseEvents](nf-uiautomationclient-iuiautomationproxyfactoryentry-put_needsadviseevents)   Sets or retrieves a value that specifies whether the proxy must be notified when an application has registered for events. (Put) |
| [IUIAutomationProxyFactoryEntry::SetWinEventsForAutomationEvent](nf-uiautomationclient-iuiautomationproxyfactoryentry-setwineventsforautomationevent)   Maps Microsoft UI Automation events to WinEvents. |

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
