# IUIAutomationSelectionPattern2

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nn-uiautomationclient-iuiautomationselectionpattern2)

# IUIAutomationSelectionPattern2 interface (uiautomationclient.h)

Extends the [IUIAutomationSelectionPattern](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationselectionpattern) interface to provide information about selected items.

## Inheritance

The **IUIAutomationSelectionPattern2** interface inherits from the IUIAutomationSelectionPattern interface.

## Methods

The **IUIAutomationSelectionPattern2** interface has these methods.

|  |
| --- |
| [IUIAutomationSelectionPattern2::get\_CachedCurrentSelectedItem](nf-uiautomationclient-iuiautomationselectionpattern2-get_cachedcurrentselecteditem)   Gets a cached IUIAutomationElement object representing the currently selected item. |
| [IUIAutomationSelectionPattern2::get\_CachedFirstSelectedItem](nf-uiautomationclient-iuiautomationselectionpattern2-get_cachedfirstselecteditem)   Gets a cached IUIAutomationElement object representing the first item in a group of selected items. |
| [IUIAutomationSelectionPattern2::get\_CachedItemCount](nf-uiautomationclient-iuiautomationselectionpattern2-get_cacheditemcount)   Gets a cached integer value indicating the number of selected items. |
| [IUIAutomationSelectionPattern2::get\_CachedLastSelectedItem](nf-uiautomationclient-iuiautomationselectionpattern2-get_cachedlastselecteditem)   Gets a cached IUIAutomationElement object representing the last item in a group of selected items. |
| [IUIAutomationSelectionPattern2::get\_CurrentCurrentSelectedItem](nf-uiautomationclient-iuiautomationselectionpattern2-get_currentcurrentselecteditem)   Gets an IUIAutomationElement object representing the currently selected item. |
| [IUIAutomationSelectionPattern2::get\_CurrentFirstSelectedItem](nf-uiautomationclient-iuiautomationselectionpattern2-get_currentfirstselecteditem)   Gets an IUIAutomationElement object representing the first item in a group of selected items. |
| [IUIAutomationSelectionPattern2::get\_CurrentItemCount](nf-uiautomationclient-iuiautomationselectionpattern2-get_currentitemcount)   Gets an integer value indicating the number of selected items. |
| [IUIAutomationSelectionPattern2::get\_CurrentLastSelectedItem](nf-uiautomationclient-iuiautomationselectionpattern2-get_currentlastselecteditem)   Gets an IUIAutomationElement object representing the last item in a group of selected items. |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 10, version 1709 [desktop apps only] |
| **Minimum supported server** | Windows Server 2016 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[IUIAutomationSelectionPattern](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationselectionpattern)

---
