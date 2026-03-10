# RespondToWinEvent

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nf-uiautomationcore-iproxyproviderwineventhandler-respondtowinevent)

# IProxyProviderWinEventHandler::RespondToWinEvent method (uiautomationcore.h)

Handles a WinEvent.

## Syntax

```
HRESULT RespondToWinEvent(
  [in] DWORD                      idWinEvent,
  [in] HWND                       hwnd,
  [in] LONG                       idObject,
  [in] LONG                       idChild,
  [in] IProxyProviderWinEventSink *pSink
);
```

## Parameters

`[in] idWinEvent`

Type: **[DWORD](/en-us/windows/desktop/WinProg/windows-data-types)**

The identifier of the incoming WinEvent. For a list of WinEvent IDs, see [Event Constants](/en-us/windows/desktop/WinAuto/event-constants).

`[in] hwnd`

Type: **[HWND](/en-us/windows/desktop/WinProg/windows-data-types)**

The handle of the window for which the WinEvent was fired. This should also be the window for which the proxy was created.

`[in] idObject`

Type: **[LONG](/en-us/windows/desktop/WinProg/windows-data-types)**

The object identifier (OBJID\_\*) of the accessible object associated with the event. For a list of object identifiers, see [Object Identifiers](/en-us/windows/desktop/WinAuto/object-identifiers).

`[in] idChild`

Type: **[LONG](/en-us/windows/desktop/WinProg/windows-data-types)**

The child identifier of the element associated with the event, or **CHILDID\_SELF** if the element is not a child.

`[in] pSink`

Type: **[IProxyProviderWinEventSink](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-iproxyproviderwineventsink)\***

A pointer to the [IProxyProviderWinEventSink](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-iproxyproviderwineventsink) interface provided by the UI Automation core. Any event that the proxy needs to raise in response to the WinEvent being handled should be added to the sink.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

The provider should review the event data. If the provider needs to raise a UI Automation event in response, the data for that event should be added to the *pSink* event sink.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[IProxyProviderWinEventHandler](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-iproxyproviderwineventhandler)

[IProxyProviderWinEventSink](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-iproxyproviderwineventsink)

**Reference**

---
