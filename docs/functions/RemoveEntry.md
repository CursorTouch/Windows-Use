# RemoveEntry

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationproxyfactorymapping-removeentry)

# IUIAutomationProxyFactoryMapping::RemoveEntry method (uiautomationclient.h)

Removes an entry from the table of proxy factories.

## Syntax

```
HRESULT RemoveEntry(
  [in] UINT index
);
```

## Parameters

`[in] index`

Type: **[UINT](/en-us/windows/desktop/WinProg/windows-data-types)**

The zero-based index of the entry to remove.

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
