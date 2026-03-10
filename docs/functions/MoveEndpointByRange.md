# MoveEndpointByRange

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationtextrange-moveendpointbyrange)

# IUIAutomationTextRange::MoveEndpointByRange method (uiautomationclient.h)

Moves one endpoint of the current text range to the specified endpoint of a second text range.

## Syntax

```
HRESULT MoveEndpointByRange(
  [in] TextPatternRangeEndpoint srcEndPoint,
  [in] IUIAutomationTextRange   *range,
  [in] TextPatternRangeEndpoint targetEndPoint
);
```

## Parameters

`[in] srcEndPoint`

Type: **[TextPatternRangeEndpoint](/en-us/windows/desktop/api/uiautomationcore/ne-uiautomationcore-textpatternrangeendpoint)**

An endpoint (either start or end) of the current text range. This is the endpoint to be moved.

`[in] range`

Type: **[IUIAutomationTextRange](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationtextrange)\***

A second text range from the same text provider as the current text range.

`[in] targetEndPoint`

Type: **[TextPatternRangeEndpoint](/en-us/windows/desktop/api/uiautomationcore/ne-uiautomationcore-textpatternrangeendpoint)**

An endpoint (either start or end) of the second text range. The *srcEndPoint* of the current text range is moved to this endpoint.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

If the endpoint being moved crosses the other endpoint of the same text range, that other endpoint is moved also, resulting in a degenerate (empty) range and ensuring the correct ordering of the endpoints (that is, the start is always less than or equal to the end).

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
