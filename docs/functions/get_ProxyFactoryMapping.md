# get_ProxyFactoryMapping

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomation-get_proxyfactorymapping)

# IUIAutomation::get\_ProxyFactoryMapping method (uiautomationclient.h)

Retrieves an object that represents the mapping of Window classnames and associated data to individual proxy factories.

This property is read-only.

## Syntax

```
HRESULT get_ProxyFactoryMapping(
  IUIAutomationProxyFactoryMapping **factoryMapping
);
```

## Parameters

`factoryMapping`

## Return value

None

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

---
