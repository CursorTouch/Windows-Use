# ISelectionItemProvider

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nn-uiautomationcore-iselectionitemprovider)

# ISelectionItemProvider interface (uiautomationcore.h)

Provides
access to individual, selectable child controls of containers that implement
[ISelectionProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-iselectionprovider).

## Inheritance

The **ISelectionItemProvider** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **ISelectionItemProvider** also has these types of members:

## Methods

The **ISelectionItemProvider** interface has these methods.

|  |
| --- |
| [ISelectionItemProvider::AddToSelection](nf-uiautomationcore-iselectionitemprovider-addtoselection)   Adds the current element to the collection of selected items. (ISelectionItemProvider.AddToSelection) |
| [ISelectionItemProvider::get\_IsSelected](nf-uiautomationcore-iselectionitemprovider-get_isselected)   Indicates whether an item is selected. |
| [ISelectionItemProvider::get\_SelectionContainer](nf-uiautomationcore-iselectionitemprovider-get_selectioncontainer)   Specifies the provider that implements ISelectionProvider and acts as the container for the calling object. |
| [ISelectionItemProvider::RemoveFromSelection](nf-uiautomationcore-iselectionitemprovider-removefromselection)   Removes the current element from the collection of selected items. |
| [ISelectionItemProvider::Select](nf-uiautomationcore-iselectionitemprovider-select)   Deselects any selected items and then selects the current element. |

## Remarks

Implemented on a Microsoft UI Automation provider that
must support the [SelectionItem](/en-us/windows/desktop/WinAuto/uiauto-implementingselectionitem) control pattern.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2003 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[UI Automation Providers Overview](/en-us/windows/desktop/WinAuto/uiauto-providersoverview)

---
