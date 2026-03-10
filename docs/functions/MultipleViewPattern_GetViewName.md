# MultipleViewPattern_GetViewName

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/nf-uiautomationcoreapi-multipleviewpattern_getviewname)

# MultipleViewPattern\_GetViewName function (uiautomationcoreapi.h)

**Note**  This function is deprecated. Client applications should use the Microsoft UI Automation Component Object Model (COM) interfaces instead.

Retrieves the name of a control-specific view.

## Syntax

```
HRESULT MultipleViewPattern_GetViewName(
  [in]  HUIAPATTERNOBJECT hobj,
  [in]  int               viewId,
  [out] BSTR              *ppStr
);
```

## Parameters

`[in] hobj`

Type: **HUIAPATTERNOBJECT**

The *control pattern* object.

`[in] viewId`

Type: **int**

The integer identifier for the view.

`[out] ppStr`

Type: **BSTR\***

When this function returns, contains a pointer to the string containing the name of the view.
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
