# TextPattern_GetSelection

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/nf-uiautomationcoreapi-textpattern_getselection)

# TextPattern\_GetSelection function (uiautomationcoreapi.h)

**Note**  This function is deprecated. Client applications should use the Microsoft UI Automation Component Object Model (COM) interfaces instead.

Gets the current range of selected text from a text container supporting the text pattern.

## Syntax

```
HRESULT TextPattern_GetSelection(
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
the text range spanning the currently selected text in the container.
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
