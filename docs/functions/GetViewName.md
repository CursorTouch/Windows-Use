# GetViewName

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nf-uiautomationcore-imultipleviewprovider-getviewname)

# IMultipleViewProvider::GetViewName method (uiautomationcore.h)

Retrieves the name of a control-specific view.

## Syntax

```
HRESULT GetViewName(
  [in]          int  viewId,
  [out, retval] BSTR *pRetVal
);
```

## Parameters

`[in] viewId`

Type: **int**

A view identifier.

`[out, retval] pRetVal`

Type: **BSTR\***

Receives a localized name for the view.
This parameter is passed uninitialized.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

View identifiers can be retrieved by using [IMultipleViewProvider::GetSupportedViews](/en-us/windows/desktop/api/uiautomationcore/nf-uiautomationcore-imultipleviewprovider-getsupportedviews).

The collection of view identifiers must be identical for all instances of a control.

View names must be suitable for use in text-to-speech, Braille, and other accessible applications.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2003 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |
| **DLL** | Uiautomationcore.dll |

## See also

[IMultipleViewProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-imultipleviewprovider)

[UI Automation Providers Overview](/en-us/windows/desktop/WinAuto/uiauto-providersoverview)

---
