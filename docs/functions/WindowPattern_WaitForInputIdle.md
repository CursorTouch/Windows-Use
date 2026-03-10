# WindowPattern_WaitForInputIdle

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/nf-uiautomationcoreapi-windowpattern_waitforinputidle)

# WindowPattern\_WaitForInputIdle function (uiautomationcoreapi.h)

**Note**  This function is deprecated. Client applications should use the Microsoft UI Automation Component Object Model (COM) interfaces instead.

Causes the calling code to block for the specified time or until the associated process enters an idle state, whichever completes first.

## Syntax

```
HRESULT WindowPattern_WaitForInputIdle(
  [in]  HUIAPATTERNOBJECT hobj,
  [in]  int               milliseconds,
  [out] BOOL              *pResult
);
```

## Parameters

`[in] hobj`

Type: **HUIAPATTERNOBJECT**

The control pattern object.

`[in] milliseconds`

Type: **int**

The number of milliseconds to wait before retrieving *pResult*.

`[out] pResult`

Type: **[BOOL](/en-us/windows/desktop/WinProg/windows-data-types)\***

**TRUE** if the window is ready to accept user input; otherwise **FALSE**.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

Returns S\_OK if successful or an error value otherwise.

## Remarks

This method is typically used in conjunction with the handling of a WindowOpenedEvent
(*Window\_WindowOpened\_Event\_GUID*).
The implementation is dependent on the underlying application framework;
therefore this method may return some time after the window is ready for user input.
The calling code should not rely on this method to ascertain exactly when the window has become idle.
Use the value of *pResult* to determine if the window is ready for input or if the method timed out.

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
