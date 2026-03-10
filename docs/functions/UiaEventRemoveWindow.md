# UiaEventRemoveWindow

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/nf-uiautomationcoreapi-uiaeventremovewindow)

# UiaEventRemoveWindow function (uiautomationcoreapi.h)

**Note**  This function is deprecated. Client applications should use the Microsoft UI Automation Component Object Model (COM) interfaces instead.

Removes a window from the event listener.

## Syntax

```
HRESULT UiaEventRemoveWindow(
  [in] HUIAEVENT hEvent,
  [in] HWND      hwnd
);
```

## Parameters

`[in] hEvent`

Type: **HUIAEVENT**

The event being listened for. This event was retrieved from [UiaAddEvent](/en-us/windows/desktop/api/uiautomationcoreapi/nf-uiautomationcoreapi-uiaaddevent).

`[in] hwnd`

Type: **[HWND](/en-us/windows/desktop/WinProg/windows-data-types)**

The handle of the window to remove.

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
