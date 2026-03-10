# GetCachedRowHeaderItems

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationtableitempattern-getcachedrowheaderitems)

# IUIAutomationTableItemPattern::GetCachedRowHeaderItems method (uiautomationclient.h)

Retrieves the cached row headers associated with a table item or cell.

## Syntax

```
HRESULT GetCachedRowHeaderItems(
  [out, retval] IUIAutomationElementArray **retVal
);
```

## Parameters

`[out, retval] retVal`

Type: **[IUIAutomationElementArray](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationelementarray)\*\***

Receives a pointer to the collection of cached row headers.

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
