# UiaDisconnectAllProviders

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/nf-uiautomationcoreapi-uiadisconnectallproviders)

# UiaDisconnectAllProviders function (uiautomationcoreapi.h)

Releases all Microsoft UI Automation resources that are held by all providers associated with the calling process.

## Syntax

```
HRESULT UiaDisconnectAllProviders();
```

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this function succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

A provider application should use this function to release UI Automation resources before shutting down.

This function cannot be called in response to a call to the [SendMessage](/en-us/windows/desktop/DevNotes/-sendmessage) function. An application cannot make outbound Component Object Model (COM) calls in response to a call to **SendMessage**, and releasing a provider is typically an outbound COM call. The **UiaDisconnectAllProviders** function returns RPC\_E\_CANTCALLOUT\_ININPUTSYNCCALL if the function is called in response to a **SendMessage** call. You can use the [InSendMessageEx](/en-us/windows/desktop/api/winuser/nf-winuser-insendmessageex) function to determine whether a particular message is being handled in response to a **SendMessage** call.

An application that calls **UiaDisconnectAllProviders** should not respond to a re-entrant [WM\_GETOBJECT](/en-us/windows/win32/winauto/wm-getobject) message by returning a pointer to the provider that it is trying to disconnect. If the application tries to disconnect a provider, but then calls the [UiaReturnRawElementProvider](/en-us/windows/desktop/api/uiautomationcoreapi/nf-uiautomationcoreapi-uiareturnrawelementprovider) function with that same provider during the disconnect attempt, the provider might not be fully disconnected.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 8 [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2012 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcoreapi.h |
| **Library** | Uiautomationcore.lib |
| **DLL** | Uiautomationcore.dll |

## See also

[Functions for Providers](/en-us/windows/desktop/WinAuto/uiauto-functions)

[UiaDisconnectProvider](/en-us/windows/desktop/api/uiautomationcoreapi/nf-uiautomationcoreapi-uiadisconnectprovider)

---
