# DockPattern_SetDockPosition

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/nf-uiautomationcoreapi-dockpattern_setdockposition)

# DockPattern\_SetDockPosition function (uiautomationcoreapi.h)

**Note**  This function is deprecated. Client applications should use the Microsoft UI Automation Component Object Model (COM) interfaces instead.

Docks the UI Automation element at the requested *dockPosition* within a docking container.

## Syntax

```
HRESULT DockPattern_SetDockPosition(
  [in] HUIAPATTERNOBJECT hobj,
  [in] DockPosition      dockPosition
);
```

## Parameters

`[in] hobj`

Type: **HUIAPATTERNOBJECT**

The *control pattern* object.

`[in] dockPosition`

Type: **[DockPosition](/en-us/windows/desktop/api/uiautomationcore/ne-uiautomationcore-dockposition)**

The location to dock the control to.

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
