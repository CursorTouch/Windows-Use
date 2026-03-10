# IDropTargetProvider

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nn-uiautomationcore-idroptargetprovider)

# IDropTargetProvider interface (uiautomationcore.h)

Enables a Microsoft UI Automation element to describe itself as an element that can receive a drop of a dragged element as part of a UI Automation drag-and-drop operation.

## Inheritance

The **IDropTargetProvider** interface inherits from the IUnknown interface.

## Methods

The **IDropTargetProvider** interface has these methods.

|  |
| --- |
| [IDropTargetProvider::get\_DropTargetEffect](nf-uiautomationcore-idroptargetprovider-get_droptargeteffect)   Retrieves a localized string that describes the effect that happens when the user drops the grabbed element on this drop target. |
| [IDropTargetProvider::get\_DropTargetEffects](nf-uiautomationcore-idroptargetprovider-get_droptargeteffects)   Retrieves an array of localized strings that enumerate the full set of effects that can happen when the user drops a grabbed element on this drop target as part of a drag-and-drop operation. (IDropTargetProvider.get\_DropTargetEffects) |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 8 [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2012 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[IDragProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-idragprovider)

[UI Automation Support for Drag-and-Drop](/en-us/windows/desktop/WinAuto/ui-automation-support-for-drag-and-drop)

---
