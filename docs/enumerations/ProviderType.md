# ProviderType

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/ne-uiautomationcoreapi-providertype)

# ProviderType enumeration (uiautomationcoreapi.h)

Contains values that specify the type of a client-side (proxy) UI Automation provider.

## Syntax

```
typedef enum ProviderType {
  ProviderType_BaseHwnd,
  ProviderType_Proxy,
  ProviderType_NonClientArea
} ;
```

## Constants

|  |
| --- |
| `ProviderType_BaseHwnd` The provider is window-based. |
| `ProviderType_Proxy` The provider is one of the Win32 or Windows Forms providers from Microsoft, or a third-party proxy provider. |
| `ProviderType_NonClientArea` The provider is a proxy for the window's non-client-area elements. |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps only] |
| **Minimum supported server** | Windows Server 2003 [desktop apps only] |
| **Header** | uiautomationcoreapi.h (include UIAutomation.h) |

---
