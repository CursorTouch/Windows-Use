# GetBoundingRectangles

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationtextrange-getboundingrectangles)

# IUIAutomationTextRange::GetBoundingRectangles method (uiautomationclient.h)

Retrieves a collection of bounding rectangles for each fully or partially visible line of text in a text range.

## Syntax

```
HRESULT GetBoundingRectangles(
  [out, retval] SAFEARRAY **boundingRects
);
```

## Parameters

`[out, retval] boundingRects`

Type: **[SAFEARRAY](/en-us/windows/win32/api/oaidl/ns-oaidl-safearray)\*\***

Receives a pointer to an array of bounding rectangles for each fully or partially visible line of text in a text range. An empty array is returned for a degenerate (empty) text range or for a text range that is completely off-screen, scrolled out of view, or obscured by an overlapping window.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

For information about how the bounding rectangles are stored in the SAFEARRAY, see [Best Practices for Using Safe Arrays](/en-us/windows/desktop/WinAuto/uiauto-workingwithsafearrays).

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

**Conceptual**

[IUIAutomationTextRange](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationtextrange)

**Reference**

[SafeArrayToRectNativeArray](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomation-safearraytorectnativearray)

[UI Automation Support for Textual Content](/en-us/windows/desktop/WinAuto/uiauto-ui-automation-textpattern-overview)

---
