# TextPattern_RangeFromPoint

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/nf-uiautomationcoreapi-textpattern_rangefrompoint)

# TextPattern\_RangeFromPoint function (uiautomationcoreapi.h)

**Note**  This function is deprecated. Client applications should use the Microsoft UI Automation Component Object Model (COM) interfaces instead.

Retrieves the degenerate (empty) text range nearest to the specified screen coordinates.

## Syntax

```
HRESULT TextPattern_RangeFromPoint(
  [in]  HUIAPATTERNOBJECT hobj,
  [in]  UiaPoint          point,
  [out] HUIATEXTRANGE     *pRetVal
);
```

## Parameters

`[in] hobj`

Type: **HUIAPATTERNOBJECT**

A control pattern object.

`[in] point`

Type: **HiaPoint**

A [UiaPoint](/en-us/windows/desktop/api/uiautomationcore/ns-uiautomationcore-uiapoint) structure that contains the location in screen coordinates.

`[out] pRetVal`

Type: **HUIATEXTRANGE\***

When this function returns, contains the text range that the node spans.
This parameter is passed uninitialized.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

Returns S\_OK if successful or an error value otherwise.

## Remarks

A text range that wraps a child object is returned if the screen coordinates are within the coordinates of an image, hyperlink, Microsoft Excel spreadsheet, or other embedded object.

Because hidden text is not ignored, this method retrieves a degenerate range from the visible text closest to the specified coordinates.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps only] |
| **Minimum supported server** | Windows Server 2003 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationcoreapi.h |
| **Library** | Uiautomationcore.lib |
| **DLL** | Uiautomationcore.dll |

---
