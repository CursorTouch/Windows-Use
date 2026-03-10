# TextRange_ExpandToEnclosingUnit

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/nf-uiautomationcoreapi-textrange_expandtoenclosingunit)

# TextRange\_ExpandToEnclosingUnit function (uiautomationcoreapi.h)

**Note**  This function is deprecated. Client applications should use the Microsoft UI Automation Component Object Model (COM) interfaces instead.

Expands the text range to a larger or smaller unit such as Character, Word, Line, or Page.

## Syntax

```
HRESULT TextRange_ExpandToEnclosingUnit(
  [in] HUIATEXTRANGE hobj,
  [in] TextUnit      unit
);
```

## Parameters

`[in] hobj`

Type: **HUIATEXTRANGE**

A text range object.

`[in] unit`

Type: **[TextUnit](/en-us/windows/desktop/api/uiautomationcore/ne-uiautomationcore-textunit)**

The unit that the provider must expand the text range to.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

Returns S\_OK if successful or an error value otherwise.

## Remarks

If the range is already an integral number of the specified units, it remains unchanged.

If the starting endpoint is not at a [TextUnit](/en-us/windows/desktop/api/uiautomationcore/ne-uiautomationcore-textunit) boundary, it is moved backward until it is at a boundary.
Subsequently, if the ending endpoint is not at a boundary, or if it is at the same boundary as the starting endpoint,
the ending endpoint is moved forward until it is at a boundary.

**Note**  It is common for a screen reader to read out a full word, entire paragraph, and so on,
at the insertion point or any virtual cursor position.

**TextRange\_ExpandToEnclosingUnit** respects both hidden and visible text. The UI Automationclient can check the is-hidden attribute (Text\_IsHidden\_Attribute\_GUID) for text visibility.

**TextRange\_ExpandToEnclosingUnit** defaults up to the next supported [TextUnit](/en-us/windows/desktop/api/uiautomationcore/ne-uiautomationcore-textunit) if the given **TextUnit** is not supported by the control.

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
