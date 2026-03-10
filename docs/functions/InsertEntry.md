# InsertEntry

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationproxyfactorymapping-insertentry)

# IUIAutomationProxyFactoryMapping::InsertEntry method (uiautomationclient.h)

Insert an entry into the table of proxy factories.

## Syntax

```
HRESULT InsertEntry(
  [in] UINT                           before,
  [in] IUIAutomationProxyFactoryEntry *factory
);
```

## Parameters

`[in] before`

Type: **[UINT](/en-us/windows/desktop/WinProg/windows-data-types)**

The zero-based index at which to insert the entry.

`[in] factory`

Type: **[IUIAutomationProxyFactoryEntry](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationproxyfactoryentry)\***

The address of the entry to insert.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

---
