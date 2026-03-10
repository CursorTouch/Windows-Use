# WaitForInputIdle

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationwindowpattern-waitforinputidle)

# IUIAutomationWindowPattern::WaitForInputIdle method (uiautomationclient.h)

Causes the calling code to block for the specified time or until the associated process enters an idle state, whichever completes first.

## Syntax

```
HRESULT WaitForInputIdle(
  [in]          int  milliseconds,
  [out, retval] BOOL *success
);
```

## Parameters

`[in] milliseconds`

Type: **int**

The amount of time, in milliseconds, to wait for the associated process to become idle.

`[out, retval] success`

Type: **[BOOL](/en-us/windows/desktop/WinProg/windows-data-types)\***

Receives the result: **TRUE** if the window has entered the idle state, or **FALSE** if the time-out occurred.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[IUIAutomationWindowPattern](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationwindowpattern)

---
