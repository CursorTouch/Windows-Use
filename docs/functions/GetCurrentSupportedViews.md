# GetCurrentSupportedViews

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationmultipleviewpattern-getcurrentsupportedviews)

# IUIAutomationMultipleViewPattern::GetCurrentSupportedViews method (uiautomationclient.h)

Retrieves a collection of control-specific view identifiers.

## Syntax

```
HRESULT GetCurrentSupportedViews(
  [out, retval] SAFEARRAY **retVal
);
```

## Parameters

`[out, retval] retVal`

Type: **[SAFEARRAY](/en-us/windows/win32/api/oaidl/ns-oaidl-safearray)\*\***

Receives a pointer to an array of view identifiers.

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

[Best Practices for Using Safe Arrays](/en-us/windows/desktop/WinAuto/uiauto-workingwithsafearrays)

[IUIAutomationMultipleViewPattern](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationmultipleviewpattern)

---
