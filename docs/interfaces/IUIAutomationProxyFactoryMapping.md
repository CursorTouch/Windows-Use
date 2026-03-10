# IUIAutomationProxyFactoryMapping

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nn-uiautomationclient-iuiautomationproxyfactorymapping)

# IUIAutomationProxyFactoryMapping interface (uiautomationclient.h)

Exposes properties and methods for a table of proxy factories. Each table entry is represented by an [IUIAutomationProxyFactoryEntry](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationproxyfactoryentry) interface. The entries are in the order in which the system will attempt to use the proxies.

## Inheritance

The **IUIAutomationProxyFactoryMapping** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **IUIAutomationProxyFactoryMapping** also has these types of members:

## Methods

The **IUIAutomationProxyFactoryMapping** interface has these methods.

|  |
| --- |
| [IUIAutomationProxyFactoryMapping::ClearTable](nf-uiautomationclient-iuiautomationproxyfactorymapping-cleartable)   Removes all entries from the proxy factory table. |
| [IUIAutomationProxyFactoryMapping::get\_Count](nf-uiautomationclient-iuiautomationproxyfactorymapping-get_count)   Retrieves the number of entries in the proxy factory table. |
| [IUIAutomationProxyFactoryMapping::GetEntry](nf-uiautomationclient-iuiautomationproxyfactorymapping-getentry)   Retrieves an entry from the proxy factory table. |
| [IUIAutomationProxyFactoryMapping::GetTable](nf-uiautomationclient-iuiautomationproxyfactorymapping-gettable)   Retrieves all entries in the proxy factory table. |
| [IUIAutomationProxyFactoryMapping::InsertEntries](nf-uiautomationclient-iuiautomationproxyfactorymapping-insertentries)   Inserts entries into the table of proxy factories. |
| [IUIAutomationProxyFactoryMapping::InsertEntry](nf-uiautomationclient-iuiautomationproxyfactorymapping-insertentry)   Insert an entry into the table of proxy factories. |
| [IUIAutomationProxyFactoryMapping::RemoveEntry](nf-uiautomationclient-iuiautomationproxyfactorymapping-removeentry)   Removes an entry from the table of proxy factories. |
| [IUIAutomationProxyFactoryMapping::RestoreDefaultTable](nf-uiautomationclient-iuiautomationproxyfactorymapping-restoredefaulttable)   Restores the default table of proxy factories. |
| [IUIAutomationProxyFactoryMapping::SetTable](nf-uiautomationclient-iuiautomationproxyfactorymapping-settable)   Sets the table of proxy factories. |

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
