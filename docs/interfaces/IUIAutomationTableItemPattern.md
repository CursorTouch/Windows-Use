# IUIAutomationTableItemPattern

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nn-uiautomationclient-iuiautomationtableitempattern)

# IUIAutomationTableItemPattern interface (uiautomationclient.h)

Provides access to a child element in a container that supports [IUIAutomationTablePattern](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationtablepattern).

## Inheritance

The **IUIAutomationTableItemPattern** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **IUIAutomationTableItemPattern** also has these types of members:

## Methods

The **IUIAutomationTableItemPattern** interface has these methods.

|  |
| --- |
| [IUIAutomationTableItemPattern::GetCachedColumnHeaderItems](nf-uiautomationclient-iuiautomationtableitempattern-getcachedcolumnheaderitems)   Retrieves the cached column headers associated with a table item or cell. |
| [IUIAutomationTableItemPattern::GetCachedRowHeaderItems](nf-uiautomationclient-iuiautomationtableitempattern-getcachedrowheaderitems)   Retrieves the cached row headers associated with a table item or cell. |
| [IUIAutomationTableItemPattern::GetCurrentColumnHeaderItems](nf-uiautomationclient-iuiautomationtableitempattern-getcurrentcolumnheaderitems)   Retrieves the column headers associated with a table item or cell. |
| [IUIAutomationTableItemPattern::GetCurrentRowHeaderItems](nf-uiautomationclient-iuiautomationtableitempattern-getcurrentrowheaderitems)   Retrieves the row headers associated with a table item or cell. |

## Remarks

Elements that support this interface must also support [IUIAutomationGridItemPattern](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationgriditempattern), to provide properties that are not specific to tables.

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
