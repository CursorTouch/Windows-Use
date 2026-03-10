# AddToSelection

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationtextrange-addtoselection)

# IUIAutomationTextRange::AddToSelection method (uiautomationclient.h)

Adds the text range to the collection of selected text ranges in a control that supports multiple, disjoint spans of selected text.

## Syntax

```
HRESULT AddToSelection();
```

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

The text insertion point moves to the newly selected text. If **AddToSelection** is called on a text range object that represents a degenerate (empty) text range, the text insertion point moves to the starting endpoint of the text range.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[IUIAutomationTextRange](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationtextrange)

[IUIAutomationTextRange::Select](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationtextrange-select)

[UI Automation Support for Textual Content](/en-us/windows/desktop/WinAuto/uiauto-ui-automation-textpattern-overview)

---
