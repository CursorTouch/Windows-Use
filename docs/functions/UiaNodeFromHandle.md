# UiaNodeFromHandle

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/nf-uiautomationcoreapi-uianodefromhandle)

# UiaNodeFromHandle function (uiautomationcoreapi.h)

**Note**  This function is deprecated. Client applications should use the Microsoft UI Automation Component Object Model (COM) interfaces instead.

Retrieves the UI Automation node associated with a window.

## Syntax

```
HRESULT UiaNodeFromHandle(
  [in]  HWND     hwnd,
  [out] HUIANODE *phnode
);
```

## Parameters

`[in] hwnd`

Type: **[HWND](/en-us/windows/desktop/WinProg/windows-data-types)**

The handle of the window.

`[out] phnode`

Type: **HUIANODE\***

The address of a variable that receives the handle of the node.
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
