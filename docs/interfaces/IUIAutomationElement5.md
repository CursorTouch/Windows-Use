# IUIAutomationElement5

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nn-uiautomationclient-iuiautomationelement5)

# IUIAutomationElement5 interface (uiautomationclient.h)

Extends the [IUIAutomationElement4](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationelement4) interface to provide access to current and cached landmark data.

## Inheritance

The **IUIAutomationElement5** interface inherits from the IUIAutomationElement4 interface.

## Methods

The **IUIAutomationElement5** interface has these methods.

|  |
| --- |
| [IUIAutomationElement5::get\_CachedLandmarkType](nf-uiautomationclient-iuiautomationelement5-get_cachedlandmarktype)   Gets the cached landmark type ID for the automation element. |
| [IUIAutomationElement5::get\_CachedLocalizedLandmarkType](nf-uiautomationclient-iuiautomationelement5-get_cachedlocalizedlandmarktype)   Gets a string containing the cached localized landmark type for the automation element. |
| [IUIAutomationElement5::get\_CurrentLandmarkType](nf-uiautomationclient-iuiautomationelement5-get_currentlandmarktype)   Gets the current landmark type ID for the automation element. |
| [IUIAutomationElement5::get\_CurrentLocalizedLandmarkType](nf-uiautomationclient-iuiautomationelement5-get_currentlocalizedlandmarktype)   Gets a string containing the current localized landmark type for the automation element. |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 10, version 1703 [desktop apps only] |
| **Minimum supported server** | Windows Server 2016 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[IUIAutomationElement4](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationelement4)

[UI Automation Element Interfaces for Clients](/en-us/windows/desktop/WinAuto/uiauto-entry-uiautoclientinterfaces)

---
