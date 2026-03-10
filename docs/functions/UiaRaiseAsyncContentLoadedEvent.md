# UiaRaiseAsyncContentLoadedEvent

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/nf-uiautomationcoreapi-uiaraiseasynccontentloadedevent)

# UiaRaiseAsyncContentLoadedEvent function (uiautomationcoreapi.h)

Called by a provider to notify the Microsoft UI Automation core that content is being loaded asynchronously.

## Syntax

```
HRESULT UiaRaiseAsyncContentLoadedEvent(
  [in] IRawElementProviderSimple *pProvider,
  [in] AsyncContentLoadedState   asyncContentLoadedState,
  [in] double                    percentComplete
);
```

## Parameters

`[in] pProvider`

Type: **[IRawElementProviderSimple](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-irawelementprovidersimple)\***

The provider node where the content is being loaded.

`[in] asyncContentLoadedState`

Type: **[AsyncContentLoadedState](/en-us/windows/desktop/api/uiautomationcoreapi/ne-uiautomationcoreapi-asynccontentloadedstate)**

The current state of loading.

`[in] percentComplete`

Type: **double**

The percentage of content that has been loaded.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this function succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2003 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcoreapi.h |
| **Library** | Uiautomationcore.lib |
| **DLL** | Uiautomationcore.dll |

---
