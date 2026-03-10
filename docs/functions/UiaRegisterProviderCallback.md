# UiaRegisterProviderCallback

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/nf-uiautomationcoreapi-uiaregisterprovidercallback)

# UiaRegisterProviderCallback function (uiautomationcoreapi.h)

**Note**  This function is deprecated. Client applications should use the Microsoft UI Automation Component Object Model (COM) interfaces instead.

Registers the application-defined method that is called by UI Automation
to obtain a provider for an element.

## Syntax

```
void UiaRegisterProviderCallback(
  [in] UiaProviderCallback *pCallback
);
```

## Parameters

`[in] pCallback`

Type: **[UiaProviderCallback](/en-us/windows/desktop/api/uiautomationcoreapi/nc-uiautomationcoreapi-uiaprovidercallback)\***

The address of the [UiaProviderCallback](/en-us/windows/desktop/api/uiautomationcoreapi/nc-uiautomationcoreapi-uiaprovidercallback) callback function that returns the provider.

## Return value

None

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps only] |
| **Minimum supported server** | Windows Server 2003 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationcoreapi.h |
| **Library** | Uiautomationcore.lib |
| **DLL** | Uiautomationcore.dll |

---
