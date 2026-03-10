# IUIAutomationElement4

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nn-uiautomationclient-iuiautomationelement4)

# IUIAutomationElement4 interface (uiautomationclient.h)

Extends the [IUIAutomationElement3](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationelement3) interface.

## Inheritance

The **IUIAutomationElement4** interface inherits from the IUIAutomationElement3 interface.

## Methods

The **IUIAutomationElement4** interface has these methods.

|  |
| --- |
| [IUIAutomationElement4::get\_CachedAnnotationObjects](nf-uiautomationclient-iuiautomationelement4-get_cachedannotationobjects)   Returns the cached list of annotation objects associated with this element, such as comment, header, footer, and so on. |
| [IUIAutomationElement4::get\_CachedAnnotationTypes](nf-uiautomationclient-iuiautomationelement4-get_cachedannotationtypes)   Returns the cached list of annotation types associated with this element, such as comment, header, footer, and so on. |
| [IUIAutomationElement4::get\_CachedLevel](nf-uiautomationclient-iuiautomationelement4-get_cachedlevel)   Returns the cached 1-based integer for the level (hierarchy) for the element. |
| [IUIAutomationElement4::get\_CachedPositionInSet](nf-uiautomationclient-iuiautomationelement4-get_cachedpositioninset)   Returns the cached 1-based integer for the ordinal position in the set for the element. |
| [IUIAutomationElement4::get\_CachedSizeOfSet](nf-uiautomationclient-iuiautomationelement4-get_cachedsizeofset)   Returns the cached 1-based integer for the size of the set where the element is located. |
| [IUIAutomationElement4::get\_CurrentAnnotationObjects](nf-uiautomationclient-iuiautomationelement4-get_currentannotationobjects)   Returns the current list of annotation objects associated with this element, such as comment, header, footer, and so on. |
| [IUIAutomationElement4::get\_CurrentAnnotationTypes](nf-uiautomationclient-iuiautomationelement4-get_currentannotationtypes)   Returns the current list of annotation types associated with this element, such as comment, header, footer, and so on. |
| [IUIAutomationElement4::get\_CurrentLevel](nf-uiautomationclient-iuiautomationelement4-get_currentlevel)   Returns the current 1-based integer for the level (hierarchy) for the element. |
| [IUIAutomationElement4::get\_CurrentPositionInSet](nf-uiautomationclient-iuiautomationelement4-get_currentpositioninset)   Returns the current 1-based integer for the ordinal position in the set for the element. |
| [IUIAutomationElement4::get\_CurrentSizeOfSet](nf-uiautomationclient-iuiautomationelement4-get_currentsizeofset)   Returns the current 1-based integer for the size of the set where the element is located. |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 10 [desktop apps only] |
| **Minimum supported server** | Windows Server 2016 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[IUIAutomationElement3](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationelement3)

[UI Automation Element Interfaces for Clients](/en-us/windows/desktop/WinAuto/uiauto-entry-uiautoclientinterfaces)

---
