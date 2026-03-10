# get_ProviderOptions

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nf-uiautomationcore-irawelementprovidersimple-get_provideroptions)

# IRawElementProviderSimple::get\_ProviderOptions method (uiautomationcore.h)

Specifies the type of Microsoft UI Automation provider; for example, whether it is a client-side (proxy) or server-side provider.

This property is read-only.

## Syntax

```
HRESULT get_ProviderOptions(
  ProviderOptions *pRetVal
);
```

## Parameters

`pRetVal`

## Return value

None

## Remarks

The method must return either [ProviderOptions\_ServerSideProvider](/en-us/windows/desktop/api/uiautomationcore/ne-uiautomationcore-provideroptions) or [ProviderOptions\_ClientSideProvider](/en-us/windows/desktop/api/uiautomationcore/ne-uiautomationcore-provideroptions).

UI Automation handles the various types of providers differently.
For example, events from a server-side provider are broadcast to all listening clients,
but events from client-side (proxy) providers remain in the client.

#### Examples

The following example implements this method for a server-side UI Automation provider.

```
HRESULT STDMETHODCALLTYPE Provider::get_ProviderOptions( ProviderOptions* pRetVal )
{
    *pRetVal = ProviderOptions_ServerSideProvider;
    return S_OK;
}
```

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2003 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[IRawElementProviderSimple](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-irawelementprovidersimple)

---
