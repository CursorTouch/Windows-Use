# WindowPattern_SetWindowVisualState

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/nf-uiautomationcoreapi-windowpattern_setwindowvisualstate)

# WindowPattern\_SetWindowVisualState function (uiautomationcoreapi.h)

**Note**  This function is deprecated. Client applications should use the Microsoft UI Automation Component Object Model (COM) interfaces instead.

Sets the visual state of a window; for example, to maximize a window.

## Syntax

```
HRESULT WindowPattern_SetWindowVisualState(
  [in] HUIAPATTERNOBJECT hobj,
  [in] WindowVisualState state
);
```

## Parameters

`[in] hobj`

Type: **HUIAPATTERNOBJECT**

The control pattern object.

`[in] state`

Type: **[WindowVisualState](/en-us/windows/desktop/api/uiautomationcore/ne-uiautomationcore-windowvisualstate)**

The visual state to set the window to.

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
