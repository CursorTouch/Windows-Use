# MoveEndpointByUnit

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationtextrange-moveendpointbyunit)

# IUIAutomationTextRange::MoveEndpointByUnit method (uiautomationclient.h)

Moves one endpoint of the text range the specified number of text units within the document range.

## Syntax

```
HRESULT MoveEndpointByUnit(
  [in]          TextPatternRangeEndpoint endpoint,
  [in]          TextUnit                 unit,
  [in]          int                      count,
  [out, retval] int                      *moved
);
```

## Parameters

`[in] endpoint`

Type: **[TextPatternRangeEndpoint](/en-us/windows/desktop/api/uiautomationcore/ne-uiautomationcore-textpatternrangeendpoint)**

A value specifying the endpoint (start or end) to move.

`[in] unit`

Type: **[TextUnit](/en-us/windows/desktop/api/uiautomationcore/ne-uiautomationcore-textunit)**

A value specifying the textual unit for moving, such as line or paragraph.

`[in] count`

Type: **int**

The number of units to move. A positive count moves the endpoint forward. A negative count moves backward. A count of 0 has no effect.

`[out, retval] moved`

Type: **int\***

Receives the count of units actually moved. This value can be less than the number requested if moving the endpoint runs into the beginning or end of the document.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

The [endpoint](/en-us/windows/desktop/api/uiautomationcore/ne-uiautomationcore-textpatternrangeendpoint) is moved forward or backward, as specified, to the next available unit boundary. If the original **endpoint** was at the boundary of the specified text unit, the **endpoint** is moved to the next available text unit boundary, as shown in the following illustration.

![Illustration showing endpoints of a text range moving](images/moveendpointbyunit.gif)
If the [endpoint](/en-us/windows/desktop/api/uiautomationcore/ne-uiautomationcore-textpatternrangeendpoint) being moved crosses the other **endpoint** of the same text range, the other **endpoint** is also moved, resulting in a degenerate range and ensuring the correct ordering of the **endpoint** (that is, that the start is always less than or equal to the end).

[MoveEndpointByUnit](/en-us/windows/desktop/api/uiautomationcore/nf-uiautomationcore-itextrangeprovider-moveendpointbyunit) deprecates up to the next supported text unit if the given text unit is not supported by the control.

The order, from smallest unit to largest, is listed here.

* *Character*
* *Format*
* *Word*
* *Line*
* *Paragraph*
* *Page*
* *Document*

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
