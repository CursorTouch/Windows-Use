# TextPattern_get_DocumentRange

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/nf-uiautomationcoreapi-textpattern_get_documentrange)

# TextPattern\_get\_DocumentRange function (uiautomationcoreapi.h)

**Note**  This function is deprecated. Client applications should use the Microsoft UI Automation Component Object Model (COM) interfaces instead.

Gets the text range for the entire document.

## Syntax

```
HRESULT TextPattern_get_DocumentRange(
  [in]  HUIAPATTERNOBJECT hobj,
  [out] HUIATEXTRANGE     *pRetVal
);
```

## Parameters

`[in] hobj`

Type: **HUIAPATTERNOBJECT**

A control pattern object.

`[out] pRetVal`

Type: **HUIATEXTRANGE\***

When this function returns, contains
the text range spanning the entire document contents of the text container.
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
