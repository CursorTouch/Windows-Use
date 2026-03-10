# IUIAutomationDropTargetPattern

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nn-uiautomationclient-iuiautomationdroptargetpattern)

# IUIAutomationDropTargetPattern interface (uiautomationclient.h)

Provides access to drag-and-drop information exposed by a Microsoft UI Automation provider for an element that can be the drop target of a drag-and-drop operation.

## Inheritance

The **IUIAutomationDropTargetPattern** interface inherits from the IUnknown interface.

## Methods

The **IUIAutomationDropTargetPattern** interface has these methods.

|  |
| --- |
| [IUIAutomationDropTargetPattern::get\_CachedDropTargetEffect](nf-uiautomationclient-iuiautomationdroptargetpattern-get_cacheddroptargeteffect)   Retrieves a cached localized string that describes what happens when the user drops the grabbed element on this drop target. |
| [IUIAutomationDropTargetPattern::get\_CachedDropTargetEffects](nf-uiautomationclient-iuiautomationdroptargetpattern-get_cacheddroptargeteffects)   Retrieves a cached array of localized strings that enumerate the full set of effects that can happen when the user drops a grabbed element on this drop target as part of a drag-and-drop operation. |
| [IUIAutomationDropTargetPattern::get\_CurrentDropTargetEffect](nf-uiautomationclient-iuiautomationdroptargetpattern-get_currentdroptargeteffect)   Retrieves a localized string that describes what happens when the user drops the grabbed element on this drop target. |
| [IUIAutomationDropTargetPattern::get\_CurrentDropTargetEffects](nf-uiautomationclient-iuiautomationdroptargetpattern-get_currentdroptargeteffects)   Retrieves an array of localized strings that enumerate the full set of effects that can happen when the user drops a grabbed element on this drop target as part of a drag-and-drop operation. (IUIAutomationDropTargetPattern.get\_CurrentDropTargetEffects) |

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
