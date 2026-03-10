# TextRange_RemoveFromSelection

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/nf-uiautomationcoreapi-textrange_removefromselection)

# TextRange\_RemoveFromSelection function (uiautomationcoreapi.h)

**Note**  This function is deprecated. Client applications should use the Microsoft UI Automation Component Object Model (COM) interfaces instead.

Removes the selected text, corresponding to the calling text range
*TextPatternRangeEndpoint\_Start*
and *TextPatternRangeEndpoint\_End*
endpoints, from an existing collection of selected text in a text container that supports multiple, disjoint selections.

## Syntax

```
HRESULT TextRange_RemoveFromSelection(
  [in] HUIATEXTRANGE hobj
);
```

## Parameters

`[in] hobj`

Type: **HUIATEXTRANGE**

A text range object.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

Returns S\_OK if successful or an error value otherwise.

## Remarks

The text insertion point will move to the area of the new selection.

Providing a degenerate text range will move the text insertion point.

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
