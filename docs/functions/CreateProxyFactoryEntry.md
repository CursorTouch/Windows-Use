# CreateProxyFactoryEntry

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomation-createproxyfactoryentry)

# IUIAutomation::CreateProxyFactoryEntry method (uiautomationclient.h)

Creates a new instance of a proxy factory object.

## Syntax

```
HRESULT CreateProxyFactoryEntry(
  [in]          IUIAutomationProxyFactory      *factory,
  [out, retval] IUIAutomationProxyFactoryEntry **factoryEntry
);
```

## Parameters

`[in] factory`

Type: **[IUIAutomationProxyFactory](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationproxyfactory)\***

A pointer to the proxy factory object.

`[out, retval] factoryEntry`

Type: **[IUIAutomationProxyFactoryEntry](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationproxyfactoryentry)\*\***

Receives a pointer to the newly created instance of the proxy factory object.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

Use the [IUIAutomationProxyFactoryMapping](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationproxyfactorymapping) interface to enter the proxy factory into the table of available proxies.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[IUIAutomation](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomation)

---
