# IsWinEventHookInstalled

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-iswineventhookinstalled)

# IsWinEventHookInstalled function (winuser.h)

Determines whether there is an installed WinEvent hook that might be notified of a specified event.

## Syntax

```
BOOL IsWinEventHookInstalled(
  [in] DWORD event
);
```

## Parameters

`[in] event`

Type: **[DWORD](/en-us/windows/desktop/WinProg/windows-data-types)**

The event constant that hooks might be notified of. The function checks whether there is an installed hook for this event constant.

## Return value

Type: **[BOOL](/en-us/windows/desktop/WinProg/windows-data-types)**

If there is a hook to be notified of the specified event, the return value is **TRUE**.

If there are no hooks to be notified of the specified event, the return value is **FALSE**.

## Remarks

This method is guaranteed to never return a false negative. If this method returns **FALSE**, it means that no hooks in the system would be notified of the event. However, this method may return a false positive. In other words, it may return **TRUE** even though there are no hooks that would be notified. Thus, it is safe for components to circumvent some work if this method returns **FALSE**.

Event hooks can be installed at any time, so server developers should not cache the return value for long periods of time.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps only] |
| **Minimum supported server** | Windows Server 2003 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | winuser.h |
| **Library** | User32.lib |
| **DLL** | User32.dll |
| **Redistributable** | Active Accessibility 2.0 RDK on Windows NT 4.0 with SP6 and later and Windows 98 |
| **API set** | ext-ms-win-ntuser-server-l1-1-1 (introduced in Windows 10, version 10.0.14393) |

## See also

[SetWinEventHook](/en-us/windows/desktop/api/winuser/nf-winuser-setwineventhook)

[UnhookWinEvent](/en-us/windows/desktop/api/winuser/nf-winuser-unhookwinevent)

---
