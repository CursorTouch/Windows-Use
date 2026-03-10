# TextRange_GetEnclosingElement

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/nf-uiautomationcoreapi-textrange_getenclosingelement)

# TextRange\_GetEnclosingElement function (uiautomationcoreapi.h)

**Note**  This function is deprecated. Client applications should use the Microsoft UI Automation Component Object Model (COM) interfaces instead.

Returns the node for the next smallest provider that covers the range.

## Syntax

```
HRESULT TextRange_GetEnclosingElement(
  [in]  HUIATEXTRANGE hobj,
  [out] HUIANODE      *pRetVal
);
```

## Parameters

`[in] hobj`

Type: **HUIATEXTRANGE**

A text range object.

`[out] pRetVal`

Type: **HUIANODE\***

When this function returns, contains
the node for the next smallest element that encloses the range.
This parameter is passed uninitialized.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

Returns S\_OK if successful or an error value otherwise.

## Remarks

The enclosing element is typically the text provider that supplies the text range. However,
if the text provider supports child elements such as tables or hyperlinks,
the enclosing element could be a descendant of the text provider.

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
