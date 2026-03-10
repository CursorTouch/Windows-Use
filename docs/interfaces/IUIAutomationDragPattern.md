# IUIAutomationDragPattern

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nn-uiautomationclient-iuiautomationdragpattern)

# IUIAutomationDragPattern interface (uiautomationclient.h)

Provides access to information exposed by a UI Automation provider for an element that can be dragged as part of a drag-and-drop operation.

## Inheritance

The **IUIAutomationDragPattern** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **IUIAutomationDragPattern** also has these types of members:

## Methods

The **IUIAutomationDragPattern** interface has these methods.

|  |
| --- |
| [IUIAutomationDragPattern::get\_CachedDropEffect](nf-uiautomationclient-iuiautomationdragpattern-get_cacheddropeffect)   Retrieves a cached localized string that indicates what happens when the user drops this element as part of a drag-and-drop operation. |
| [IUIAutomationDragPattern::get\_CachedDropEffects](nf-uiautomationclient-iuiautomationdragpattern-get_cacheddropeffects)   Retrieves a cached array of localized strings that enumerate the full set of effects that can happen when the user drops this element as part of a drag-and-drop operation. |
| [IUIAutomationDragPattern::get\_CachedIsGrabbed](nf-uiautomationclient-iuiautomationdragpattern-get_cachedisgrabbed)   Retrieves a cached value that indicates whether this element has been grabbed as part of a drag-and-drop operation. |
| [IUIAutomationDragPattern::get\_CurrentDropEffect](nf-uiautomationclient-iuiautomationdragpattern-get_currentdropeffect)   Retrieves a localized string that indicates what happens when the user drops this element as part of a drag-drop operation. |
| [IUIAutomationDragPattern::get\_CurrentDropEffects](nf-uiautomationclient-iuiautomationdragpattern-get_currentdropeffects)   Retrieves an array of localized strings that enumerate the full set of effects that can happen when this element as part of a drag-and-drop operation. |
| [IUIAutomationDragPattern::get\_CurrentIsGrabbed](nf-uiautomationclient-iuiautomationdragpattern-get_currentisgrabbed)   Indicates whether the user has grabbed this element as part of a drag-and-drop operation. |
| [IUIAutomationDragPattern::GetCachedGrabbedItems](nf-uiautomationclient-iuiautomationdragpattern-getcachedgrabbeditems)   Retrieves a cached collection of elements that represent the full set of items that the user is dragging as part of a drag operation. |
| [IUIAutomationDragPattern::GetCurrentGrabbedItems](nf-uiautomationclient-iuiautomationdragpattern-getcurrentgrabbeditems)   Retrieves a collection of elements that represent the full set of items that the user is dragging as part of a drag operation. |

## Remarks

Microsoft UI Automation clients use this interface to access the dragging properties and functionality of a control or UI element that the user can drag-and-drop on a drop target.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 8 [desktop apps only] |
| **Minimum supported server** | Windows Server 2012 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[Control Pattern Interfaces for Clients](/en-us/windows/desktop/WinAuto/uiauto-client-controlpatterninterfaces)

[UI Automation Support for Drag-and-Drop](/en-us/windows/desktop/WinAuto/ui-automation-support-for-drag-and-drop)

---
