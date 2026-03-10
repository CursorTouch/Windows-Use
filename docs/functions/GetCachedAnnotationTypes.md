# GetCachedAnnotationTypes

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationspreadsheetitempattern-getcachedannotationtypes)

# IUIAutomationSpreadsheetItemPattern::GetCachedAnnotationTypes method (uiautomationclient.h)

Retrieves a cached array of annotation type identifiers indicating the types of annotations that are associated with this spreadsheet cell.

## Syntax

```
HRESULT GetCachedAnnotationTypes(
  [out, retval] SAFEARRAY **retVal
);
```

## Parameters

`[out, retval] retVal`

Type: **[SAFEARRAY](/en-us/windows/win32/api/oaidl/ns-oaidl-safearray)\*\***

Receives the cached array of annotation type identifiers. For a list of possible values, see [Annotation Type Identifiers](/en-us/windows/desktop/WinAuto/uiauto-annotation-type-identifiers).

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

[Best Practices for Using Safe Arrays](/en-us/windows/desktop/WinAuto/uiauto-workingwithsafearrays)

[IUIAutomationSpreadsheetItemPattern](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationspreadsheetitempattern)

---
