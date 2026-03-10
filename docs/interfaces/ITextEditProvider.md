# ITextEditProvider

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nn-uiautomationcore-itexteditprovider)

# ITextEditProvider interface (uiautomationcore.h)

Extends the [ITextProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-itextprovider) interface to enable Microsoft UI Automation providers to expose programmatic text-edit actions.

## Inheritance

The **ITextEditProvider** interface inherits from [ITextProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-itextprovider). **ITextEditProvider** also has these types of members:

## Methods

The **ITextEditProvider** interface has these methods.

|  |
| --- |
| [ITextEditProvider::GetActiveComposition](nf-uiautomationcore-itexteditprovider-getactivecomposition)   Returns the active composition. (ITextEditProvider.GetActiveComposition) |
| [ITextEditProvider::GetConversionTarget](nf-uiautomationcore-itexteditprovider-getconversiontarget)   Returns the current conversion target range. (ITextEditProvider.GetConversionTarget) |

## Remarks

Call the [UiaRaiseTextEditTextChangedEvent](/en-us/windows/desktop/api/uiautomationcoreapi/nf-uiautomationcoreapi-uiaraisetextedittextchangedevent) function to raise the UI Automation events that notify clients of changes. Use values of [TextEditChangeType](/en-us/windows/desktop/api/uiautomationcore/ne-uiautomationcore-texteditchangetype) to describe the change. Follow the guidance given in [TextEdit Control Pattern](/en-us/windows/desktop/WinAuto/textedit-control-pattern) that describes when to raise the events and what payload the events should pass to UI Automation.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 8.1 [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2012 R2 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[ITextProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-itextprovider)

[TextEdit Control Pattern](/en-us/windows/desktop/WinAuto/textedit-control-pattern)

[UI Automation Providers Overview](/en-us/windows/desktop/WinAuto/uiauto-providersoverview)

[UI Automation Support for Textual Content](/en-us/windows/desktop/WinAuto/uiauto-ui-automation-textpattern-overview)

[UiaRaiseTextEditTextChangedEvent](/en-us/windows/desktop/api/uiautomationcoreapi/nf-uiautomationcoreapi-uiaraisetextedittextchangedevent)

---
