# UiaDisconnectProvider

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/nf-uiautomationcoreapi-uiadisconnectprovider)

# UiaDisconnectProvider function (uiautomationcoreapi.h)

Releases all references that a particular provider holds to Microsoft UI Automation objects.

## Syntax

```
HRESULT UiaDisconnectProvider(
  [in] IRawElementProviderSimple *pProvider
);
```

## Parameters

`[in] pProvider`

Type: **[IRawElementProviderSimple](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-irawelementprovidersimple)\***

The provider to be disconnected.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this function succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

A provider should call this function to clean up UI Automation resources that are associated with a UI element that was destroyed. The DLL associated with the UI element can be safely unloaded after the function returns.

After this function returns, all client requests that are associated with the disconnected provider receive the [UIA\_E\_ELEMENTNOTAVAILABLE](/en-us/windows/desktop/WinAuto/uiauto-error-codes)
error code.

This function cannot be called in response to a call to the [SendMessage](/en-us/windows/desktop/DevNotes/-sendmessage) function. An application cannot make outbound Component Object Model (COM) calls in response to a call to **SendMessage**, and releasing a provider is typically an outbound COM call. The **UiaDisconnectProvider** function returns RPC\_E\_CANTCALLOUT\_ININPUTSYNCCALL if the function is called in response to a **SendMessage** call. You can use the [InSendMessageEx](/en-us/windows/desktop/api/winuser/nf-winuser-insendmessageex) function to determine whether a particular message is being handled in response to a **SendMessage** call.

An application that calls **UiaDisconnectProvider** should not respond to a re-entrant [WM\_GETOBJECT](/en-us/windows/win32/winauto/wm-getobject) message by returning a pointer to the provider that it is trying to disconnect. If the application tries to disconnect a provider, but then calls the [UiaReturnRawElementProvider](/en-us/windows/desktop/api/uiautomationcoreapi/nf-uiautomationcoreapi-uiareturnrawelementprovider) function with that same provider during the disconnect attempt, the provider might not be fully disconnected.

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

[UiaDisconnectAllProviders](/en-us/windows/desktop/api/uiautomationcoreapi/nf-uiautomationcoreapi-uiadisconnectallproviders)

---
