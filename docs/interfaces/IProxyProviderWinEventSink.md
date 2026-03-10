# IProxyProviderWinEventSink

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nn-uiautomationcore-iproxyproviderwineventsink)

# IProxyProviderWinEventSink interface (uiautomationcore.h)

Exposes methods used by proxy providers to raise events.

## Inheritance

The **IProxyProviderWinEventSink** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **IProxyProviderWinEventSink** also has these types of members:

## Methods

The **IProxyProviderWinEventSink** interface has these methods.

|  |
| --- |
| [IProxyProviderWinEventSink::AddAutomationEvent](nf-uiautomationcore-iproxyproviderwineventsink-addautomationevent)   Raises a Microsoft UI Automation event. |
| [IProxyProviderWinEventSink::AddAutomationPropertyChangedEvent](nf-uiautomationcore-iproxyproviderwineventsink-addautomationpropertychangedevent)   Raises a property-changed event. |
| [IProxyProviderWinEventSink::AddStructureChangedEvent](nf-uiautomationcore-iproxyproviderwineventsink-addstructurechangedevent)   Raises an event to notify clients that the structure of the UI Automation tree has changed. |

## Remarks

The **IProxyProviderWinEventSink** interface is provided by UIAutomationCore.dll when the framework calls the [IProxyProviderWinEventHandler::RespondToWinEvent](/en-us/windows/desktop/api/uiautomationcore/nf-uiautomationcore-iproxyproviderwineventhandler-respondtowinevent) method. The framework stores the events added to the **IProxyProviderWinEventSink** object. When **IProxyProviderWinEventHandler::RespondToWinEvent** returns, the framework passes the events back to the client side, where the UI Automation events are actually fired.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

---
