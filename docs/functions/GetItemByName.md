# GetItemByName

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nf-uiautomationcore-ispreadsheetprovider-getitembyname)

# ISpreadsheetProvider::GetItemByName method (uiautomationcore.h)

Exposes a UI Automation element that represents the spreadsheet cell that has the specified name.

## Syntax

```
HRESULT GetItemByName(
  [in]          LPCWSTR                   name,
  [out, retval] IRawElementProviderSimple **pRetVal
);
```

## Parameters

`[in] name`

Type: **LPCWSTR**

The name of the target cell.

`[out, retval] pRetVal`

Type: **[IRawElementProviderSimple](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-irawelementprovidersimple)\*\***

Receives the element that represents the target cell.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

A spreadsheet cell typically has a name such as âc5â or âa15â. A name can also apply to a range of cells.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 8 [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2012 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[ISpreadsheetProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-ispreadsheetprovider)

---
