# ProviderOptions

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/ne-uiautomationcore-provideroptions)

# ProviderOptions enumeration (uiautomationcore.h)

Contains values that specify the type of UI Automation provider. The [IRawElementProviderSimple::ProviderOptions](/en-us/windows/desktop/api/uiautomationcore/nf-uiautomationcore-irawelementprovidersimple-get_provideroptions) property uses this enumeration.

## Syntax

```
typedef enum ProviderOptions {
  ProviderOptions_ClientSideProvider = 0x1,
  ProviderOptions_ServerSideProvider = 0x2,
  ProviderOptions_NonClientAreaProvider = 0x4,
  ProviderOptions_OverrideProvider = 0x8,
  ProviderOptions_ProviderOwnsSetFocus = 0x10,
  ProviderOptions_UseComThreading = 0x20,
  ProviderOptions_RefuseNonClientSupport = 0x40,
  ProviderOptions_HasNativeIAccessible = 0x80,
  ProviderOptions_UseClientCoordinates = 0x100
} ;
```

## Constants

|  |
| --- |
| `ProviderOptions_ClientSideProvider` Value: *0x1* The provider is a client-side (proxy) provider. |
| `ProviderOptions_ServerSideProvider` Value: *0x2* The provider is a server-side provider. |
| `ProviderOptions_NonClientAreaProvider` Value: *0x4* The provider is a non-client-area provider. |
| `ProviderOptions_OverrideProvider` Value: *0x8* The provider overrides another provider. |
| `ProviderOptions_ProviderOwnsSetFocus` Value: *0x10* The provider handles its own focus, and does not want UI Automation to set focus to the nearest window on its behalf. This option is typically used by providers for windows that appear to take focus without actually receiving Win32 focus, such as menus and drop-downs. |
| `ProviderOptions_UseComThreading` Value: *0x20* The provider has explicit support for COM threading models, so that calls by UI Automation on COM-based providers are received on the appropriate thread. This means that STA-based provider implementations will be called back on their own STA thread, and therefore do not need extra synchronization to safely access resources that belong to that STA. MTA-based provider implementations will be called back on some other thread in the MTA, and will require appropriate synchronization to be added, as is usual for MTA code. |
| `ProviderOptions_RefuseNonClientSupport` Value: *0x40* The provider handles its own non-client area and does not want UI Automation to provide default accessibility support for controls in the non-client area, such as minimize/maximize buttons and menu bars. |
| `ProviderOptions_HasNativeIAccessible` Value: *0x80* The provider implements the [IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible) interface. |
| `ProviderOptions_UseClientCoordinates` Value: *0x100* The provider works in client coordinates instead of screen coordinates. |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps only] |
| **Minimum supported server** | Windows Server 2003 [desktop apps only] |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[SetFocus](/en-us/windows/desktop/api/uiautomationcore/nf-uiautomationcore-irawelementproviderfragment-setfocus)

---
