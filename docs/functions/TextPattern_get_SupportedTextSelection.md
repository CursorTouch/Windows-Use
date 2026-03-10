# TextPattern_get_SupportedTextSelection

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/nf-uiautomationcoreapi-textpattern_get_supportedtextselection)

# TextPattern\_get\_SupportedTextSelection function (uiautomationcoreapi.h)

Important

This function is deprecated. Client applications should use the Microsoft UI Automation Component Object Model (COM) interfaces instead.

Ascertains whether the text container's contents can be selected and deselected.

## Syntax

```
HRESULT TextPattern_get_SupportedTextSelection(
  [in]  HUIAPATTERNOBJECT      hobj,
  [out] SupportedTextSelection *pRetVal
);
```

## Parameters

`[in] hobj`

Type: **HUIAPATTERNOBJECT**

A control pattern object.

`[out] pRetVal`

Type: **[BOOL](/en-us/windows/desktop/WinProg/windows-data-types)\***

When this function returns, contains a value indicating whether the text container can have its contents selected and deselected.

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
