# RangeFromPoint

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationtextpattern-rangefrompoint)

# IUIAutomationTextPattern::RangeFromPoint method (uiautomationclient.h)

Retrieves the degenerate (empty) text range nearest to the specified screen coordinates.

## Syntax

```
HRESULT RangeFromPoint(
  [in]          POINT                  pt,
  [out, retval] IUIAutomationTextRange **range
);
```

## Parameters

`[in] pt`

Type: **[POINT](/en-us/windows/win32/api/windef/ns-windef-point)**

A structure that contains the location, in screen coordinates.

`[out, retval] range`

Type: **[IUIAutomationTextRange](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationtextrange)\*\***

Receives a pointer to the degenerate text range nearest the specified location.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

A text range that wraps a child object is returned if the screen coordinates are within the coordinates of an image, hyperlink, Microsoft Excel spreadsheet, or other embedded object.

Because hidden text is not ignored, this method retrieves a degenerate range from the visible text closest to the specified coordinates.

The implementation of **RangeFromPoint** in Windows Internet Explorer 9 does not return the expected result. Instead, clients should:

1. Call the [GetVisibleRanges](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationtextpattern-getvisibleranges) method to retrieve an array of visible text ranges.
2. For each text range in the array, call [IUIAutomationTextRange::GetBoundingRectangles](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationtextrange-getboundingrectangles) to retrieve the bounding rectangles.
3. Check the bounding rectangles to find the text range that occupies the particular screen coordinates.

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
