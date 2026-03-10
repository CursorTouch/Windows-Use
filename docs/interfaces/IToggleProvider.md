# IToggleProvider

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nn-uiautomationcore-itoggleprovider)

# IToggleProvider interface (uiautomationcore.h)

Provides access to
controls that can cycle through a set of states and maintain a state after it is set.

## Inheritance

The **IToggleProvider** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **IToggleProvider** also has these types of members:

## Methods

The **IToggleProvider** interface has these methods.

|  |
| --- |
| [IToggleProvider::get\_ToggleState](nf-uiautomationcore-itoggleprovider-get_togglestate)   Specifies the toggle state of the control. |
| [IToggleProvider::Toggle](nf-uiautomationcore-itoggleprovider-toggle)   Cycles through the toggle states of a control. |

## Remarks

Implemented on a Microsoft UI Automation provider that must support the [Toggle](/en-us/windows/desktop/WinAuto/uiauto-implementingtoggle) control pattern.

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
