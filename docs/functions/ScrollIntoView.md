# ScrollIntoView

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationtextrange-scrollintoview)

# IUIAutomationTextRange::ScrollIntoView method (uiautomationclient.h)

Causes the text control to scroll until the text range is visible in the viewport.

## Syntax

```
HRESULT ScrollIntoView(
  [in] BOOL alignToTop
);
```

## Parameters

`[in] alignToTop`

Type: **[BOOL](/en-us/windows/desktop/WinProg/windows-data-types)**

**TRUE** if the text control should be scrolled so that the text range is flush with the top of the viewport; **FALSE** if it should be flush with the bottom of the viewport.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

The method respects both hidden and visible text. If the text range is hidden, the text control will scroll only if the hidden text has an anchor in the viewport.

A Microsoft UI Automation client can check text visibility by calling [IUIAutomationTextRange::GetAttributeValue](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationtextrange-getattributevalue) with the *attr* parameter set to [UIA\_IsHiddenAttributeId](/en-us/windows/desktop/WinAuto/uiauto-textattribute-ids).

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
