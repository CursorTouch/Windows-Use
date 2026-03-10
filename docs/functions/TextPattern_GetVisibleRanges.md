# TextPattern_GetVisibleRanges

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/nf-uiautomationcoreapi-textpattern_getvisibleranges)

# TextPattern\_GetVisibleRanges function (uiautomationcoreapi.h)

**Note**  This function is deprecated. Client applications should use the Microsoft UI Automation Component Object Model (COM) interfaces instead.

Retrieves an array of disjoint text ranges from a text container where each
text range begins with the first partially visible line through to the end of the
last partially visible line. For example, a multi-column layout where the columns
are partially scrolled out of the visible area of the viewport and the content
flows from the bottom of one column to the top of the next.

## Syntax

```
HRESULT TextPattern_GetVisibleRanges(
  [in]  HUIAPATTERNOBJECT hobj,
  [out] SAFEARRAY         **pRetVal
);
```

## Parameters

`[in] hobj`

Type: **HUIAPATTERNOBJECT**

A control pattern object.

`[out] pRetVal`

Type: **HUIATEXTRANGE\***

When this function returns, contains
an array of text ranges spanning the visible text within the text container.
This parameter is passed uninitialized.

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
