# IDragProvider

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nn-uiautomationcore-idragprovider)

# IDragProvider interface (uiautomationcore.h)

Enables a Microsoft UI Automation element to describe itself as an element that can be dragged as part of a drag-and-drop operation.

## Inheritance

The **IDragProvider** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **IDragProvider** also has these types of members:

## Methods

The **IDragProvider** interface has these methods.

|  |
| --- |
| [IDragProvider::get\_DropEffect](nf-uiautomationcore-idragprovider-get_dropeffect)   Retrieves a localized string that indicates what happens when this element is dropped as part of a drag-drop operation. |
| [IDragProvider::get\_DropEffects](nf-uiautomationcore-idragprovider-get_dropeffects)   Retrieves an array of localized strings that enumerate the full set of effects that can happen when this element is dropped as part of a drag-and-drop operation. |
| [IDragProvider::get\_IsGrabbed](nf-uiautomationcore-idragprovider-get_isgrabbed)   Indicates whether the element has been grabbed as part of a drag-and-drop operation. |
| [IDragProvider::GetGrabbedItems](nf-uiautomationcore-idragprovider-getgrabbeditems)   Retrieves the collection of elements that are being dragged as part of a drag operation. |

## Remarks

A provider can implement **IDragProvider** only on the element being dragged, or it can use an intermediary drag object that implements **IDragProvider**, in addition to the **IDragProvider** implementation on the individual element. The intermediary is responsible for firing all events, which enables the provider to support dragging multiple elements at once, and to describe the multi-element drag operation with a single set of drag properties and events.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 8 [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2012 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[IDropTargetProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-idroptargetprovider)

[UI Automation Support for Drag-and-Drop](/en-us/windows/desktop/WinAuto/ui-automation-support-for-drag-and-drop)

---
