# UiaHostProviderFromHwnd

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/nf-uiautomationcoreapi-uiahostproviderfromhwnd)

# UiaHostProviderFromHwnd function (uiautomationcoreapi.h)

Gets the host provider for a window.

## Syntax

```
HRESULT UiaHostProviderFromHwnd(
  [in]  HWND                      hwnd,
  [out] IRawElementProviderSimple **ppProvider
);
```

## Parameters

`[in] hwnd`

Type: **[HWND](/en-us/windows/desktop/WinProg/windows-data-types)**

The window containing the element served by the provider.

`[out] ppProvider`

Type: **[IRawElementProviderSimple](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-irawelementprovidersimple)\*\***

The host provider for the window.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this function succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

The object retrieved by this function is useful only for responding to calls to the [IRawElementProviderSimple::get\_HostRawElementProvider](/en-us/windows/desktop/api/uiautomationcore/nf-uiautomationcore-irawelementprovidersimple-get_hostrawelementprovider) method. You cannot use the object to raise events, provide properties, and so on. If you need to raise events or provide properties, you must create a provider object that fully implements the [IRawElementProviderSimple](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-irawelementprovidersimple) interface.

#### Examples

The following example returns the host provider for the window that hosts the control served by
this provider.

```
HRESULT STDMETHODCALLTYPE Provider::get_HostRawElementProvider(IRawElementProviderSimple** pRetVal)
{
    return UiaHostProviderFromHwnd(controlHWnd, pRetVal); 
}
```

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2003 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcoreapi.h |
| **Library** | Uiautomationcore.lib |
| **DLL** | Uiautomationcore.dll |

## See also

[Functions for Providers](/en-us/windows/desktop/WinAuto/uiauto-functions)

---
