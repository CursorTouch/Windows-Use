# IUIAutomationCacheRequest

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nn-uiautomationclient-iuiautomationcacherequest)

# IUIAutomationCacheRequest interface (uiautomationclient.h)

Exposes properties and methods of a cache request. Client applications use this interface to specify the properties and control patterns to be cached when a Microsoft UI Automation element is obtained.

## Inheritance

The **IUIAutomationCacheRequest** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **IUIAutomationCacheRequest** also has these types of members:

## Methods

The **IUIAutomationCacheRequest** interface has these methods.

|  |
| --- |
| [IUIAutomationCacheRequest::AddPattern](nf-uiautomationclient-iuiautomationcacherequest-addpattern)   Adds a control pattern to the cache request. |
| [IUIAutomationCacheRequest::AddProperty](nf-uiautomationclient-iuiautomationcacherequest-addproperty)   Adds a property to the cache request. |
| [IUIAutomationCacheRequest::Clone](nf-uiautomationclient-iuiautomationcacherequest-clone)   Creates a copy of the cache request. |
| [IUIAutomationCacheRequest::get\_AutomationElementMode](nf-uiautomationclient-iuiautomationcacherequest-get_automationelementmode)   Indicates whether returned elements contain full references to the underlying UI, or only cached information. (Get) |
| [IUIAutomationCacheRequest::get\_TreeFilter](nf-uiautomationclient-iuiautomationcacherequest-get_treefilter)   Specifies the view of the UI Automation element tree that is used when caching. (Get) |
| [IUIAutomationCacheRequest::get\_TreeScope](nf-uiautomationclient-iuiautomationcacherequest-get_treescope)   Specifies the scope of caching. (Get) |
| [IUIAutomationCacheRequest::put\_AutomationElementMode](nf-uiautomationclient-iuiautomationcacherequest-put_automationelementmode)   Indicates whether returned elements contain full references to the underlying UI, or only cached information. (Put) |
| [IUIAutomationCacheRequest::put\_TreeFilter](nf-uiautomationclient-iuiautomationcacherequest-put_treefilter)   Specifies the view of the UI Automation element tree that is used when caching. (Put) |
| [IUIAutomationCacheRequest::put\_TreeScope](nf-uiautomationclient-iuiautomationcacherequest-put_treescope)   Specifies the scope of caching. (Put) |

## Remarks

Retrieving properties and control patterns through UI Automation requires cross-process calls that can slow down performance. By caching values of proprieties and control patterns in a batch operation, you can enhance the performance of your application.

Create a new cache request by calling [CreateCacheRequest](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomation-createcacherequest), and configure the request by calling methods of **IUIAutomationCacheRequest**.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[UI Automation Element Interfaces for Clients](/en-us/windows/desktop/WinAuto/uiauto-entry-uiautoclientinterfaces)

---
