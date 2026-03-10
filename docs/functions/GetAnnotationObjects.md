# GetAnnotationObjects

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nf-uiautomationcore-ispreadsheetitemprovider-getannotationobjects)

# ISpreadsheetItemProvider::GetAnnotationObjects method (uiautomationcore.h)

Retrieves an array of objects that represent the annotations associated with this spreadsheet cell.

## Syntax

```
HRESULT GetAnnotationObjects(
  [out, retval] SAFEARRAY **pRetVal
);
```

## Parameters

`[out, retval] pRetVal`

Type: **[SAFEARRAY](/en-us/windows/win32/api/oaidl/ns-oaidl-safearray)\*\***

Receives an array of [IRawElementProviderSimple](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-irawelementprovidersimple) interfaces that represent the annotations associated with the spreadsheet cell.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 8 [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2012 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[Best Practices for Using Safe Arrays](/en-us/windows/desktop/WinAuto/uiauto-workingwithsafearrays)

[ISpreadsheetItemProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-ispreadsheetitemprovider)

---
