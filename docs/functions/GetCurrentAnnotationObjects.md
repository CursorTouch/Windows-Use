# GetCurrentAnnotationObjects

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationspreadsheetitempattern-getcurrentannotationobjects)

# IUIAutomationSpreadsheetItemPattern::GetCurrentAnnotationObjects method (uiautomationclient.h)

Retrieves an array of elements representing the annotations associated with this spreadsheet cell.

## Syntax

```
HRESULT GetCurrentAnnotationObjects(
  [out, retval] IUIAutomationElementArray **retVal
);
```

## Parameters

`[out, retval] retVal`

Type: **[IUIAutomationElementArray](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationelementarray)\*\***

Receives the array of annotation elements for this spreadsheet cell.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 8 [desktop apps only] |
| **Minimum supported server** | Windows Server 2012 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[IUIAutomationSpreadsheetItemPattern](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationspreadsheetitempattern)

---
