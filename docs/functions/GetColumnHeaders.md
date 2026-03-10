# GetColumnHeaders

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nf-uiautomationcore-itableprovider-getcolumnheaders)

# ITableProvider::GetColumnHeaders method (uiautomationcore.h)

Gets a collection of Microsoft UI Automation providers
that represents all the column headers in a table.

## Syntax

```
HRESULT GetColumnHeaders(
  [out, retval] SAFEARRAY **pRetVal
);
```

## Parameters

`[out, retval] pRetVal`

Type: **[SAFEARRAY](/en-us/windows/win32/api/oaidl/ns-oaidl-safearray)\*\***

Receives a pointer to a [SAFEARRAY](/en-us/windows/win32/api/oaidl/ns-oaidl-safearray) that contains an array of pointers to the [IRawElementProviderSimple](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-irawelementprovidersimple) interfaces
of the column headers. This parameter is passed uninitialized.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2003 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[Best Practices for Using Safe Arrays](/en-us/windows/desktop/WinAuto/uiauto-workingwithsafearrays)

**Conceptual**

[ITableProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-itableprovider)

**Reference**

[UI Automation Providers Overview](/en-us/windows/desktop/WinAuto/uiauto-providersoverview)

---
