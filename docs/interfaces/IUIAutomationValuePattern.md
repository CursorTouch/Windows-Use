# IUIAutomationValuePattern

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nn-uiautomationclient-iuiautomationvaluepattern)

# IUIAutomationValuePattern interface (uiautomationclient.h)

Provides access to a control that contains a value that does not span a range and that can be represented as a string. This string may or may not be editable, depending on the control and its settings.

## Inheritance

The **IUIAutomationValuePattern** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **IUIAutomationValuePattern** also has these types of members:

## Methods

The **IUIAutomationValuePattern** interface has these methods.

|  |
| --- |
| [IUIAutomationValuePattern::get\_CachedIsReadOnly](nf-uiautomationclient-iuiautomationvaluepattern-get_cachedisreadonly)   Retrieves a cached value that indicates whether the value of the element is read-only. |
| [IUIAutomationValuePattern::get\_CachedValue](nf-uiautomationclient-iuiautomationvaluepattern-get_cachedvalue)   Retrieves the cached value of the element. |
| [IUIAutomationValuePattern::get\_CurrentIsReadOnly](nf-uiautomationclient-iuiautomationvaluepattern-get_currentisreadonly)   Indicates whether the value of the element is read-only. |
| [IUIAutomationValuePattern::get\_CurrentValue](nf-uiautomationclient-iuiautomationvaluepattern-get_currentvalue)   Retrieves the value of the element. |
| [IUIAutomationValuePattern::SetValue](nf-uiautomationclient-iuiautomationvaluepattern-setvalue)   Sets the value of the element. |

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
