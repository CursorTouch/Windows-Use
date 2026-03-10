# IUIAutomationTextChildPattern

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nn-uiautomationclient-iuiautomationtextchildpattern)

# IUIAutomationTextChildPattern interface (uiautomationclient.h)

Provides access a text-based control (or an object embedded in text) that is a child or descendant of another text-based control.

## Inheritance

The **IUIAutomationTextChildPattern** interface inherits from the IUnknown interface.

## Methods

The **IUIAutomationTextChildPattern** interface has these methods.

|  |
| --- |
| [IUIAutomationTextChildPattern::get\_TextContainer](nf-uiautomationclient-iuiautomationtextchildpattern-get_textcontainer)   Retrieves this element's nearest ancestor element that supports the Text control pattern. |
| [IUIAutomationTextChildPattern::get\_TextRange](nf-uiautomationclient-iuiautomationtextchildpattern-get_textrange)   Retrieves a text range that encloses this child element. (IUIAutomationTextChildPattern.get\_TextRange) |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 8 [desktop apps only] |
| **Minimum supported server** | Windows Server 2012 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[Control Pattern Interfaces for Clients](/en-us/windows/desktop/WinAuto/uiauto-client-controlpatterninterfaces)

---
