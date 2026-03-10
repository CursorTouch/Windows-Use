# GetSelection

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nf-uiautomationcore-itextprovider-getselection)

# ITextProvider::GetSelection method (uiautomationcore.h)

Retrieves a collection of text ranges that represents the currently selected text in a text-based control.

## Syntax

```
HRESULT GetSelection(
  [out, retval] SAFEARRAY **pRetVal
);
```

## Parameters

`[out, retval] pRetVal`

Type: **[SAFEARRAY](/en-us/windows/win32/api/oaidl/ns-oaidl-safearray)\*\***

Receives the address of an array of pointers to the [ITextRangeProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-itextrangeprovider) interfaces of the text ranges,
one for each selected span of text. This parameter is passed uninitialized.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

For UI Automation providers that support text selection,
the provider should implement this method and also return a [ITextProvider::SupportedTextSelection](/en-us/windows/desktop/api/uiautomationcore/nf-uiautomationcore-itextprovider-get_supportedtextselection) value.

If the control contains only a single span of selected text, the *pRetVal* array should contain a single text range.

If the control contains a text insertion point but no text is selected, the *pRetVal* array should contain a degenerate (empty) text range at the position of the text insertion point.

If the control contains no selected text, or if the control does not contain a text insertion point, set *pRetVal* to **NULL**.

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

[ITextProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-itextprovider)

[ITextRangeProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-itextrangeprovider)

**Reference**

[UI Automation Providers Overview](/en-us/windows/desktop/WinAuto/uiauto-providersoverview)

---
