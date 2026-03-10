# GetCurrentColumnHeaders

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationtablepattern-getcurrentcolumnheaders)

# IUIAutomationTablePattern::GetCurrentColumnHeaders method (uiautomationclient.h)

Retrieves a collection of UI Automation elements representing all the column headers in a table.

## Syntax

```
HRESULT GetCurrentColumnHeaders(
  [out, retval] IUIAutomationElementArray **retVal
);
```

## Parameters

`[out, retval] retVal`

Type: **[IUIAutomationElementArray](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationelementarray)\*\***

Receives a pointer to the collection of column headers. The default is an empty array.

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

## See also

[IUIAutomationTablePattern](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationtablepattern)

[IUIAutomationTablePattern::GetCurrentRowHeaders](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationtablepattern-getcurrentrowheaders)

---
