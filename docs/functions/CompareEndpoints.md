# CompareEndpoints

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nf-uiautomationcore-itextrangeprovider-compareendpoints)

# ITextRangeProvider::CompareEndpoints method (uiautomationcore.h)

Returns a value that specifies whether two text ranges have identical endpoints.

## Syntax

```
HRESULT CompareEndpoints(
  [in]          TextPatternRangeEndpoint endpoint,
  [in]          ITextRangeProvider       *targetRange,
  [in]          TextPatternRangeEndpoint targetEndpoint,
  [out, retval] int                      *pRetVal
);
```

## Parameters

`[in] endpoint`

Type: **[TextPatternRangeEndpoint](/en-us/windows/desktop/api/uiautomationcore/ne-uiautomationcore-textpatternrangeendpoint)**

The endpoint (starting or ending) of the caller's text range.

`[in] targetRange`

Type: **[ITextRangeProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-itextrangeprovider)\***

The text range to be compared.

`[in] targetEndpoint`

Type: **[TextPatternRangeEndpoint](/en-us/windows/desktop/api/uiautomationcore/ne-uiautomationcore-textpatternrangeendpoint)**

The endpoint (starting or ending) of the target text range.

`[out, retval] pRetVal`

Type: **int\***

Receives a value that indicates whether the two text ranges have identical endpoints.
This parameter is passed uninitialized.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

Returns a negative value if the caller's endpoint occurs earlier in the text than the target endpoint.

Returns zero if the caller's endpoint is at the same location as the target endpoint.

Returns a positive value if the caller's endpoint occurs later in the text than the target endpoint.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2003 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

**Conceptual**

[ITextProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-itextprovider)

[ITextRangeProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-itextrangeprovider)

**Reference**

[UI Automation Providers Overview](/en-us/windows/desktop/WinAuto/uiauto-providersoverview)

---
