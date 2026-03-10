# GetCaretRange

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationtextpattern2-getcaretrange)

# IUIAutomationTextPattern2::GetCaretRange method (uiautomationclient.h)

Retrieves a zero-length text range at the location of the caret that belongs to the text-based control.

## Syntax

```
HRESULT GetCaretRange(
  [out, retval] BOOL                   *isActive,
  [out, retval] IUIAutomationTextRange **range
);
```

## Parameters

`[out, retval] isActive`

Type: **BOOL\***

**TRUE** if the text-based control that contains the caret has keyboard focus, otherwise **FALSE**.

`[out, retval] range`

Type: **[IUIAutomationTextRange](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationtextrange)\*\***

Receives a text range that represents the current location of the caret that belongs to the text-based control.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

If the *isActive* parameter is **FALSE**, the caret that belongs to the text-based control might not be at the same location as the system caret.

This method retrieves a text range that a client can use to find the bounding rectangle of the caret belonging to the text-based control, or to find the text near the caret.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 8 [desktop apps only] |
| **Minimum supported server** | Windows Server 2012 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[IUIAutomationTextPattern2](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationtextpattern2)

[UI Automation Support for Textual Content](/en-us/windows/desktop/WinAuto/uiauto-ui-automation-textpattern-overview)

[Working with Text-based Controls](/en-us/windows/desktop/WinAuto/uiauto-workingwithtextbasedcontrols)

---
