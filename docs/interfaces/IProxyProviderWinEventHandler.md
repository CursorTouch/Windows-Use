# IProxyProviderWinEventHandler

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nn-uiautomationcore-iproxyproviderwineventhandler)

# IProxyProviderWinEventHandler interface (uiautomationcore.h)

Exposes a method that is implemented by proxy providers to handle WinEvents. To implement Microsoft UI Automation event handling, a proxy provider may need to handle WinEvents that are raised by the proxied UI. UI Automation will use the **IProxyProviderWinEventHandler** interface to notify the provider that a WinEvent has been raised for the provider window.

## Inheritance

The **IProxyProviderWinEventHandler** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **IProxyProviderWinEventHandler** also has these types of members:

## Methods

The **IProxyProviderWinEventHandler** interface has these methods.

|  |
| --- |
| [IProxyProviderWinEventHandler::RespondToWinEvent](nf-uiautomationcore-iproxyproviderwineventhandler-respondtowinevent)   Handles a WinEvent. |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

---
