# GetVisibleRanges

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationtextpattern-getvisibleranges)

# IUIAutomationTextPattern::GetVisibleRanges method (uiautomationclient.h)

Retrieves an array of disjoint text ranges from a text-based control where each text range represents a contiguous span of visible text.

## Syntax

```
HRESULT GetVisibleRanges(
  [out, retval] IUIAutomationTextRangeArray **ranges
);
```

## Parameters

`[out, retval] ranges`

Type: **[IUIAutomationTextRangeArray](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationtextrangearray)\*\***

Receives a pointer to the collection of visible text ranges within the text-based control.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

If the visible text consists of one contiguous span of text, the *ranges* array will contain a single text range that represents all of the visible text.

If the visible text consists of multiple, disjoint spans of text, the *ranges* array will contain one text range for each visible span, beginning with the first visible span, and ending with the last visible span. Disjoint spans of visible text can occur when the content of a text-based control is partially obscured
by an overlapping window or other object, or when a text-based control with multiple pages or columns
has content that is partially scrolled out of view.

**IUIAutomationTextPattern::GetVisibleRanges** retrieves a degenerate (empty) text range if no text is visible, if all text is scrolled out of view, or if the text-based control contains no text.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[IUIAutomationTextPattern](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationtextpattern)

[UI Automation Support for Textual Content](/en-us/windows/desktop/WinAuto/uiauto-ui-automation-textpattern-overview)

---
