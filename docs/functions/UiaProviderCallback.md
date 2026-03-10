# UiaProviderCallback

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/nc-uiautomationcoreapi-uiaprovidercallback)

# UiaProviderCallback callback function (uiautomationcoreapi.h)

**Note**  This function is deprecated. Client applications should use the Microsoft UI Automation Component Object Model (COM) interfaces instead.

An application-defined function that is called by UI Automation
to obtain a client-side provider for an element.

## Syntax

```
UiaProviderCallback Uiaprovidercallback;

SAFEARRAY * Uiaprovidercallback(
  [in] HWND hwnd,
  [in] ProviderType providerType
)
{...}
```

## Parameters

`[in] hwnd`

Type: **[HWND](/en-us/windows/desktop/WinProg/windows-data-types)**

The handle of the window served by the provider.

`[in] providerType`

Type: **[ProviderType](/en-us/windows/desktop/api/uiautomationcoreapi/ne-uiautomationcoreapi-providertype)**

A value from the [ProviderType](/en-us/windows/desktop/api/uiautomationcoreapi/ne-uiautomationcoreapi-providertype) enumerated type specifying the type of provider that is being requested.

## Return value

Type: **[SAFEARRAY](/en-us/windows/win32/api/oaidl/ns-oaidl-safearray)**

A [SAFEARRAY](/en-us/windows/win32/api/oaidl/ns-oaidl-safearray) containing the requested provider.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps only] |
| **Minimum supported server** | Windows Server 2003 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationcoreapi.h |

---
