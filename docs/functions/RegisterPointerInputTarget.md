# RegisterPointerInputTarget

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-registerpointerinputtarget)

# RegisterPointerInputTarget function (winuser.h)

Allows the caller to register a target window to which all pointer input of the specified type is redirected.

## Syntax

```
BOOL RegisterPointerInputTarget(
  [in] HWND               hwnd,
  [in] POINTER_INPUT_TYPE pointerType
);
```

## Parameters

`[in] hwnd`

The window to register as a global redirection target.

Redirection can cause the foreground window to lose activation (focus). To avoid this, ensure the window is a message-only window or has the [WS\_EX\_NOACTIVATE](/en-us/windows/desktop/winmsg/extended-window-styles) style set.

`[in] pointerType`

Type of pointer input to be redirected to the specified window. This is any valid and supported value from the [POINTER\_INPUT\_TYPE](/en-us/windows/win32/api/winuser/ne-winuser-tagpointer_input_type) enumeration. Note that the generic **PT\_POINTER** type and the **PT\_MOUSE** type are not valid in this parameter.

## Return value

If the function succeeds, the return value is non-zero.

If the function fails, the return value is zero. To get extended error information, call [GetLastError](/en-us/windows/desktop/api/errhandlingapi/nf-errhandlingapi-getlasterror).

## Remarks

An application with the UI Access privilege can use this function to register its own window to receive all input of the specified pointer input type. Each desktop allows only one such global redirection target window for each pointer input type at any given time. The first window to successfully register remains in effect until the window is unregistered or destroyed, at which point the role is available to the next qualified caller.

While the registration is in effect, all input of the specified pointer type, whether from an input device or injected by an application, is redirected to the registered window. However, when the process that owns the registered window injects input of the specified pointer type, such injected is not redirected but is instead processed normally.

An application that wishes to register the same window as a global redirection target for multiple pointer input types must call the **RegisterPointerInputTarget** function multiple times, once for each pointer input type of interest.

If the calling thread does not have the UI Access privilege, this function fails with the last error set to **ERROR\_ACCESS\_DENIED**.

If the specified pointer input type is not valid, this function fails with the last error set to **ERROR\_INVALID\_PARAMETER**.

If the calling thread does not own the specified window, this function fails with the last error set to **ERROR\_ACCESS\_DENIED**.

If the specified windowâs desktop already has a registered global redirection target for the specified pointer input type, this function fails with the last error set to **ERROR\_ACCESS\_DENIED**.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 8 [desktop apps only] |
| **Minimum supported server** | Windows Server 2012 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | winuser.h (include Windows.h) |
| **Library** | User32.lib |
| **DLL** | User32.dll |

---
