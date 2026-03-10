# TextRange_GetBoundingRectangles

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/nf-uiautomationcoreapi-textrange_getboundingrectangles)

# TextRange\_GetBoundingRectangles function (uiautomationcoreapi.h)

**Note**  This function is deprecated. Client applications should use the Microsoft UI Automation Component Object Model (COM) interfaces instead.

Retrieves the minimum number of bounding rectangles that can enclose the range, one rectangle per line.

## Syntax

```
HRESULT TextRange_GetBoundingRectangles(
  [in]  HUIATEXTRANGE hobj,
  [out] SAFEARRAY     **pRetVal
);
```

## Parameters

`[in] hobj`

Type: **HUIATEXTRANGE**

A text range object.

`[out] pRetVal`

Type: **[SAFEARRAY](/en-us/windows/win32/api/oaidl/ns-oaidl-safearray)\*\***

When this function returns, contains
an array of rectangle coordinates for the lines of text that the range spans.
This parameter is passed uninitialized.
The SAFEARRAY contains VARIANTs of type VT\_I4.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

Returns S\_OK if successful or an error value otherwise.

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
