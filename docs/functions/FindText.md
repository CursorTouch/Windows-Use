# FindText

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationtextrange-findtext)

# IUIAutomationTextRange::FindText method (uiautomationclient.h)

Retrieves a text range subset that contains the specified text.

## Syntax

```
HRESULT FindText(
  [in]          BSTR                   text,
  [in]          BOOL                   backward,
  [in]          BOOL                   ignoreCase,
  [out, retval] IUIAutomationTextRange **found
);
```

## Parameters

`[in] text`

Type: **BSTR**

The text to find.

`[in] backward`

Type: **[BOOL](/en-us/windows/desktop/WinProg/windows-data-types)**

**TRUE** if the last occurring text range should be returned instead of the first; otherwise **FALSE**.

`[in] ignoreCase`

Type: **[BOOL](/en-us/windows/desktop/WinProg/windows-data-types)**

**TRUE** if case should be ignored; otherwise **FALSE**.

`[out, retval] found`

Type: **[IUIAutomationTextRange](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationtextrange)\*\***

Receives a pointer to the text range, or **NULL** if no match is found.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

There is no differentiation between hidden and visible text.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[IUIAutomationTextRange](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationtextrange)

[UI Automation Support for Textual Content](/en-us/windows/desktop/WinAuto/uiauto-ui-automation-textpattern-overview)

---
