# Move

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationtextrange-move)

# IUIAutomationTextRange::Move method (uiautomationclient.h)

Moves the text range forward or backward by the specified number of text units .

## Syntax

```
HRESULT Move(
  [in]          TextUnit unit,
  [in]          int      count,
  [out, retval] int      *moved
);
```

## Parameters

`[in] unit`

Type: **[TextUnit](/en-us/windows/desktop/api/uiautomationcore/ne-uiautomationcore-textunit)**

A value specifying the type of text units, such as character, word, paragraph, and so on.

`[in] count`

Type: **int**

The number of text units to move. A positive value moves the text range forward. A negative value moves the text range backward. Zero has no effect.

`[out, retval] moved`

Type: **int\***

Receives the number of text units actually moved. This can be less than the number requested if either of the new text range endpoints is greater than or less than the endpoints retrieved by the [IUIAutomationTextPattern::DocumentRange](/en-us/windows/desktop/api/uiautomationcore/nf-uiautomationcore-itextprovider-get_documentrange) method. This value can be negative if navigation is happening in the backward direction.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

**IUIAutomationTextRange::Move** moves the text range to span a different part of the text; it does not alter the text in any way.

For a non-degenerate (non-empty) text range, **IUIAutomationTextRange::Move** normalizes and moves the range by performing the following steps.

1. The text range is collapsed to a degenerate (empty) range at the starting endpoint.
2. If necessary, the resulting text range is moved backward in the document to the beginning of the requested text unit boundary.
3. The text range is moved forward or backward in the document by the requested number of text unit boundaries.
4. The text range is expanded from the degenerate state by moving the ending endpoint forward by one requested text unit boundary.

If any of the preceding steps fail, the text range is left unchanged. If the text range cannot be moved as far as the requested number of text units, but can be moved by a smaller number of text units, the text range is moved by the smaller number of text units and *moved* is set to the number of text units moved.

For a degenerate text range, **IUIAutomationTextRange::Move** simply moves the text insertion point by the specified number of text units.

When moving a text range, **IUIAutomationTextRange::Move** ignores the boundaries of any embedded objects in the text.

**IUIAutomationTextRange::Move** respects both hidden and visible text.

If a text-based control does not support the text unit specified by the *unit* parameter, **IUIAutomationTextRange::Move** substitutes the next larger supported text unit.

The size of the text units, from smallest unit to largest, is as follows.

* Character
* Format
* Word
* Line
* Paragraph
* Page
* Document

### Range behavior when *unit* is `TextUnit::Format`

`TextUnit::Format` as a *unit* value positions the boundary of a text range to expand or move the range based on shared text attributes (format) of the text within the range. However, using the format text unit will not move or expand a text range across the boundary of an embedded object, such as an image or hyperlink. For more info, see [UI Automation Text Units](/en-us/windows/desktop/WinAuto/uiauto-uiautomationtextunits) or [UI Automation Support for Textual Content](/en-us/windows/desktop/WinAuto/uiauto-ui-automation-textpattern-overview).

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
