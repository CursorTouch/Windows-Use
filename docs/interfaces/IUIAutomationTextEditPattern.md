# IUIAutomationTextEditPattern

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nn-uiautomationclient-iuiautomationtexteditpattern)

# IUIAutomationTextEditPattern interface (uiautomationclient.h)

Provides access to a control that modifies text, for example a control that performs auto-correction or enables input composition through an Input Method Editor (IME).

## Inheritance

The **IUIAutomationTextEditPattern** interface inherits from [IUIAutomationTextPattern](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationtextpattern). **IUIAutomationTextEditPattern** also has these types of members:

## Methods

The **IUIAutomationTextEditPattern** interface has these methods.

|  |
| --- |
| [IUIAutomationTextEditPattern::GetActiveComposition](nf-uiautomationclient-iuiautomationtexteditpattern-getactivecomposition)   Returns the active composition. (IUIAutomationTextEditPattern.GetActiveComposition) |
| [IUIAutomationTextEditPattern::GetConversionTarget](nf-uiautomationclient-iuiautomationtexteditpattern-getconversiontarget)   Returns the current conversion target range. (IUIAutomationTextEditPattern.GetConversionTarget) |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 8.1 [desktop apps only] |
| **Minimum supported server** | Windows Server 2012 R2 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[Control Pattern Interfaces for Clients](/en-us/windows/desktop/WinAuto/uiauto-client-controlpatterninterfaces)

[IUIAutomationTextPattern](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationtextpattern)

---
