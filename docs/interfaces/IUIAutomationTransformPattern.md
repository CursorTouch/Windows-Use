# IUIAutomationTransformPattern

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nn-uiautomationclient-iuiautomationtransformpattern)

# IUIAutomationTransformPattern interface (uiautomationclient.h)

Provides access to a control that can be moved, resized, or rotated.

## Inheritance

The **IUIAutomationTransformPattern** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **IUIAutomationTransformPattern** also has these types of members:

## Methods

The **IUIAutomationTransformPattern** interface has these methods.

|  |
| --- |
| [IUIAutomationTransformPattern::get\_CachedCanMove](nf-uiautomationclient-iuiautomationtransformpattern-get_cachedcanmove)   Retrieves a cached value that indicates whether the element can be moved. |
| [IUIAutomationTransformPattern::get\_CachedCanResize](nf-uiautomationclient-iuiautomationtransformpattern-get_cachedcanresize)   Retrieves a cached value that indicates whether the element can be resized. |
| [IUIAutomationTransformPattern::get\_CachedCanRotate](nf-uiautomationclient-iuiautomationtransformpattern-get_cachedcanrotate)   Retrieves a cached value that indicates whether the element can be rotated. |
| [IUIAutomationTransformPattern::get\_CurrentCanMove](nf-uiautomationclient-iuiautomationtransformpattern-get_currentcanmove)   Indicates whether the element can be moved. |
| [IUIAutomationTransformPattern::get\_CurrentCanResize](nf-uiautomationclient-iuiautomationtransformpattern-get_currentcanresize)   Indicates whether the element can be resized. |
| [IUIAutomationTransformPattern::get\_CurrentCanRotate](nf-uiautomationclient-iuiautomationtransformpattern-get_currentcanrotate)   Indicates whether the element can be rotated. |
| [IUIAutomationTransformPattern::Move](nf-uiautomationclient-iuiautomationtransformpattern-move)   Moves the UI Automation element. |
| [IUIAutomationTransformPattern::Resize](nf-uiautomationclient-iuiautomationtransformpattern-resize)   Resizes the UI Automation element. |
| [IUIAutomationTransformPattern::Rotate](nf-uiautomationclient-iuiautomationtransformpattern-rotate)   Rotates the UI Automation element. |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[Control Pattern Interfaces for Clients](/en-us/windows/desktop/WinAuto/uiauto-client-controlpatterninterfaces)

---
