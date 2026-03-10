# UnhookWinEvent

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-unhookwinevent)

# UnhookWinEvent function (winuser.h)

Removes an event hook function created by a previous call to [SetWinEventHook](/en-us/windows/desktop/api/winuser/nf-winuser-setwineventhook).

## Syntax

```
BOOL UnhookWinEvent(
  [in] HWINEVENTHOOK hWinEventHook
);
```

## Parameters

`[in] hWinEventHook`

Type: **HWINEVENTHOOK**

Handle to the event hook returned in the previous call to [SetWinEventHook](/en-us/windows/desktop/api/winuser/nf-winuser-setwineventhook).

## Return value

Type: **[BOOL](/en-us/windows/desktop/WinProg/windows-data-types)**

If successful, returns **TRUE**; otherwise, returns **FALSE**.

Three common errors cause this function to fail:

* The *hWinEventHook* parameter is **NULL** or not valid.
* The event hook specified by *hWinEventHook* was already removed.
* **UnhookWinEvent** is called from a thread that is different from the original call to [SetWinEventHook](/en-us/windows/desktop/api/winuser/nf-winuser-setwineventhook).

## Remarks

This function removes the event hook specified by *hWinEventHook* that prevents the corresponding callback function from receiving further event notifications. If the client's thread ends, the system automatically calls this function.

Call this function from the same thread that installed the event hook. **UnhookWinEvent** fails if called from a thread different from the call that corresponds to [SetWinEventHook](/en-us/windows/desktop/api/winuser/nf-winuser-setwineventhook).

If WINEVENT\_INCONTEXT was specified when this event hook was installed, the system attempts to unload the corresponding DLL from all processes that loaded it. Although unloading does not occur immediately, the hook function is not called after **UnhookWinEvent** returns. For more information on WINEVENT\_INCONTEXT, see [In-Context Hook Functions](/en-us/windows/desktop/WinAuto/in-context-hook-functions).

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 2000 Professional [desktop apps only] |
| **Minimum supported server** | Windows Server 2003 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | winuser.h (include Windows.h) |
| **Library** | User32.lib |
| **DLL** | User32.dll |
| **Redistributable** | Active Accessibility 1.3 RDK on Windows NT 4.0 with SP6 and later and Windows 95 |

---
