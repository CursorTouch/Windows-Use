# TransformPattern_Move

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/nf-uiautomationcoreapi-transformpattern_move)

# TransformPattern\_Move function (uiautomationcoreapi.h)

**Note**  This function is deprecated. Client applications should use the Microsoft UI Automation Component Object Model (COM) interfaces instead.

Moves an element to a specified location on the screen.

## Syntax

```
HRESULT TransformPattern_Move(
  [in] HUIAPATTERNOBJECT hobj,
  [in] double            x,
  [in] double            y
);
```

## Parameters

`[in] hobj`

Type: **HUIAPATTERNOBJECT**

The control pattern object.

`[in] x`

Type: **double**

The horizontal screen coordinate to move the element to.

`[in] y`

Type: **double**

The vertical screen coordinate to move the element to.

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
