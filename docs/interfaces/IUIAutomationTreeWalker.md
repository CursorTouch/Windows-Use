# IUIAutomationTreeWalker

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nn-uiautomationclient-iuiautomationtreewalker)

# IUIAutomationTreeWalker interface (uiautomationclient.h)

Exposes properties and methods that UI Automation client applications use to view and navigate the UI Automation elements on the desktop.

## Inheritance

The **IUIAutomationTreeWalker** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **IUIAutomationTreeWalker** also has these types of members:

## Methods

The **IUIAutomationTreeWalker** interface has these methods.

|  |
| --- |
| [IUIAutomationTreeWalker::get\_Condition](nf-uiautomationclient-iuiautomationtreewalker-get_condition)   Retrieves the condition that defines the view of the UI Automation tree. |
| [IUIAutomationTreeWalker::GetFirstChildElement](nf-uiautomationclient-iuiautomationtreewalker-getfirstchildelement)   Retrieves the first child element of the specified UI Automation element. |
| [IUIAutomationTreeWalker::GetFirstChildElementBuildCache](nf-uiautomationclient-iuiautomationtreewalker-getfirstchildelementbuildcache)   Retrieves the first child element of the specified UI Automation element, and caches properties and control patterns. |
| [IUIAutomationTreeWalker::GetLastChildElement](nf-uiautomationclient-iuiautomationtreewalker-getlastchildelement)   Retrieves the last child element of the specified UI Automation element. |
| [IUIAutomationTreeWalker::GetLastChildElementBuildCache](nf-uiautomationclient-iuiautomationtreewalker-getlastchildelementbuildcache)   Retrieves the last child element of the specified UI Automation element, and caches properties and control patterns. |
| [IUIAutomationTreeWalker::GetNextSiblingElement](nf-uiautomationclient-iuiautomationtreewalker-getnextsiblingelement)   Retrieves the next sibling element of the specified UI Automation element. |
| [IUIAutomationTreeWalker::GetNextSiblingElementBuildCache](nf-uiautomationclient-iuiautomationtreewalker-getnextsiblingelementbuildcache)   Retrieves the next sibling element of the specified UI Automation element, and caches properties and control patterns. |
| [IUIAutomationTreeWalker::GetParentElement](nf-uiautomationclient-iuiautomationtreewalker-getparentelement)   Retrieves the parent element of the specified UI Automation element. |
| [IUIAutomationTreeWalker::GetParentElementBuildCache](nf-uiautomationclient-iuiautomationtreewalker-getparentelementbuildcache)   Retrieves the parent element of the specified UI Automation element, and caches properties and control patterns. |
| [IUIAutomationTreeWalker::GetPreviousSiblingElement](nf-uiautomationclient-iuiautomationtreewalker-getprevioussiblingelement)   Retrieves the previous sibling element of the specified UI Automation element. |
| [IUIAutomationTreeWalker::GetPreviousSiblingElementBuildCache](nf-uiautomationclient-iuiautomationtreewalker-getprevioussiblingelementbuildcache)   Retrieves the previous sibling element of the specified UI Automation element, and caches properties and control patterns. |
| [IUIAutomationTreeWalker::NormalizeElement](nf-uiautomationclient-iuiautomationtreewalker-normalizeelement)   Retrieves the ancestor element nearest to the specified Microsoft UI Automation element in the tree view. |
| [IUIAutomationTreeWalker::NormalizeElementBuildCache](nf-uiautomationclient-iuiautomationtreewalker-normalizeelementbuildcache)   Retrieves the ancestor element nearest to the specified Microsoft UI Automation element in the tree view, prefetches the requested properties and control patterns, and stores the prefetched items in the cache. |

## Remarks

UI Automation clients view the elements on the desktop as a set of [IUIAutomation](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomation) objects arranged in a tree structure. Using the **IUIAutomationTreeWalker** interface, a client application can navigate by selecting a view of the tree and stepping from one element to another in a specified direction using methods such as [GetFirstChildElement](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationtreewalker-getfirstchildelement) and [GetNextSiblingElement](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationtreewalker-getnextsiblingelement).

Navigating the tree using **IUIAutomationTreeWalker** can result in cross-process calls and is not as efficient as locating an element using the [IUIAutomationElement::FindAll](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-findall) or [IUIAutomationElement::FindFirst](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-findfirst) methods.

If your client application might try to find elements in its own user interface, you must make all UI Automation calls on a separate thread.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[CreateTreeWalker](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomation-createtreewalker)

[UI Automation Element Interfaces for Clients](/en-us/windows/desktop/WinAuto/uiauto-entry-uiautoclientinterfaces)

---
