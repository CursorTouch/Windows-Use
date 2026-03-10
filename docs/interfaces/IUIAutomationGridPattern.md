# IUIAutomationGridPattern

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nn-uiautomationclient-iuiautomationgridpattern)

# IUIAutomationGridPattern interface (uiautomationclient.h)

Provides access to a control that acts as a container for a collection of child controls that are organized in a two-dimensional logical coordinate system that can be traversed by row and column. The children of this element support the [IUIAutomationGridItemPattern](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationgriditempattern) interface.

## Inheritance

The **IUIAutomationGridPattern** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **IUIAutomationGridPattern** also has these types of members:

## Methods

The **IUIAutomationGridPattern** interface has these methods.

|  |
| --- |
| [IUIAutomationGridPattern::get\_CachedColumnCount](nf-uiautomationclient-iuiautomationgridpattern-get_cachedcolumncount)   Retrieves the cached number of columns in the grid. |
| [IUIAutomationGridPattern::get\_CachedRowCount](nf-uiautomationclient-iuiautomationgridpattern-get_cachedrowcount)   Retrieves the cached number of rows in the grid. |
| [IUIAutomationGridPattern::get\_CurrentColumnCount](nf-uiautomationclient-iuiautomationgridpattern-get_currentcolumncount)   The number of columns in the grid. |
| [IUIAutomationGridPattern::get\_CurrentRowCount](nf-uiautomationclient-iuiautomationgridpattern-get_currentrowcount)   Retrieves the number of rows in the grid. |
| [IUIAutomationGridPattern::GetItem](nf-uiautomationclient-iuiautomationgridpattern-getitem)   Retrieves a UI Automation element representing an item in the grid. |

## Remarks

This interface does not support active manipulation of a grid; the [IUIAutomationTransformPattern](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationtransformpattern) interface is required for this functionality.

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
