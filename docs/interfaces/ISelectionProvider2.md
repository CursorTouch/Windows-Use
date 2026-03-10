# ISelectionProvider2

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nn-uiautomationcore-iselectionprovider2)

# ISelectionProvider2 interface (uiautomationcore.h)

Extends the [ISelectionItemProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-iselectionitemprovider) interface to provide information about selected items.

## Inheritance

The **ISelectionProvider2** interface inherits from the ISelectionProvider interface.

## Methods

The **ISelectionProvider2** interface has these methods.

|  |
| --- |
| [ISelectionProvider2::get\_CurrentSelectedItem](nf-uiautomationcore-iselectionprovider2-get_currentselecteditem)   Gets the currently selected item. |
| [ISelectionProvider2::get\_FirstSelectedItem](nf-uiautomationcore-iselectionprovider2-get_firstselecteditem)   Gets the first item in a group of selected items. |
| [ISelectionProvider2::get\_ItemCount](nf-uiautomationcore-iselectionprovider2-get_itemcount)   Gets the number of selected items. |
| [ISelectionProvider2::get\_LastSelectedItem](nf-uiautomationcore-iselectionprovider2-get_lastselecteditem)   Gets the last item in a group of selected items. |

## Remarks

This interface is implemented by a Microsoft UI Automation provider.

Providers should raise an event of type [UIA\_Selection\_InvalidatedEventId](/en-us/windows/desktop/WinAuto/uiauto-event-ids) when a selection in a container has changed significantly.

When selecting from a list or 2D grid there are primary pieces of information that ATs would like to better read to their end users. Using Excel as a primary example, there are 4 main pieces of information necessary for the AT to provide a good experience:

* The first cell in the selection
* The last cell in the selection
* The current item as you select
* The total count

![Image of an Excel spreadsheet showing multiple cells selected. Selection starts in the upper right on cell F5 and ends in the lower left on cell D7.](images/iselectionpattern2.png)
The above image illustrates the end state of a 2D selection:

* The user started in cell F5 (note this is where focus input stays because if you type that is where data lands)
* The user selects down the column to cell F7
* The user then selects left to cell D7

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 10, version 1709 [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2016 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[ISelectionItemProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-iselectionitemprovider)

[UI Automation Providers Overview](/en-us/windows/desktop/WinAuto/uiauto-providersoverview)

---
