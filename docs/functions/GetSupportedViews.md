# GetSupportedViews

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nf-uiautomationcore-imultipleviewprovider-getsupportedviews)

# IMultipleViewProvider::GetSupportedViews method (uiautomationcore.h)

Retrieves a collection of control-specific view identifiers.

## Syntax

```
HRESULT GetSupportedViews(
  [out, retval] SAFEARRAY **pRetVal
);
```

## Parameters

`[out, retval] pRetVal`

Type: **[SAFEARRAY](/en-us/windows/win32/api/oaidl/ns-oaidl-safearray)\*\***

Receives a collection of control-specific integer values that identify the views available for a UI Automation element.
This parameter is passed uninitialized.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

An empty array is returned by UIAutoCore.dll if the provider does not supply any view identifiers.

The collection of view identifiers must be identical for all instances of a control.

View identifier values can be passed to [IMultipleViewProvider::GetViewName](/en-us/windows/desktop/api/uiautomationcore/nf-uiautomationcore-imultipleviewprovider-getviewname).

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2003 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |
| **DLL** | Uiautomationcore.dll |

## See also

[Best Practices for Using Safe Arrays](/en-us/windows/desktop/WinAuto/uiauto-workingwithsafearrays)

**Conceptual**

[IMultipleViewProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-imultipleviewprovider)

**Reference**

[UI Automation Providers Overview](/en-us/windows/desktop/WinAuto/uiauto-providersoverview)

---
