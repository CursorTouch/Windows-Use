# IUIAutomationTogglePattern

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nn-uiautomationclient-iuiautomationtogglepattern)

# IUIAutomationTogglePattern interface (uiautomationclient.h)

Provides access to a control that can cycle through a set of states, and maintain a state after it is set.

## Inheritance

The **IUIAutomationTogglePattern** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **IUIAutomationTogglePattern** also has these types of members:

## Methods

The **IUIAutomationTogglePattern** interface has these methods.

|  |
| --- |
| [IUIAutomationTogglePattern::get\_CachedToggleState](nf-uiautomationclient-iuiautomationtogglepattern-get_cachedtogglestate)   Retrieves the cached state of the control. |
| [IUIAutomationTogglePattern::get\_CurrentToggleState](nf-uiautomationclient-iuiautomationtogglepattern-get_currenttogglestate)   Retrieves the state of the control. |
| [IUIAutomationTogglePattern::Toggle](nf-uiautomationclient-iuiautomationtogglepattern-toggle)   Cycles through the toggle states of the control. |

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
