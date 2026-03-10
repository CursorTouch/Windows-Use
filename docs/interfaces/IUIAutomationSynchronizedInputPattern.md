# IUIAutomationSynchronizedInputPattern

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nn-uiautomationclient-iuiautomationsynchronizedinputpattern)

# IUIAutomationSynchronizedInputPattern interface (uiautomationclient.h)

Provides access to the keyboard or mouse input of a control.

## Inheritance

The **IUIAutomationSynchronizedInputPattern** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **IUIAutomationSynchronizedInputPattern** also has these types of members:

## Methods

The **IUIAutomationSynchronizedInputPattern** interface has these methods.

|  |
| --- |
| [IUIAutomationSynchronizedInputPattern::Cancel](nf-uiautomationclient-iuiautomationsynchronizedinputpattern-cancel)   Causes the Microsoft UI Automation provider to stop listening for mouse or keyboard input. |
| [IUIAutomationSynchronizedInputPattern::StartListening](nf-uiautomationclient-iuiautomationsynchronizedinputpattern-startlistening)   Causes the Microsoft UI Automation provider to start listening for mouse or keyboard input. |

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
