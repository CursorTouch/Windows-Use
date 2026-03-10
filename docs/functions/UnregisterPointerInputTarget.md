# UnregisterPointerInputTarget

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-unregisterpointerinputtarget)

# UnregisterPointerInputTarget function (winuser.h)

Allows the caller to unregister a target window to which all pointer input of the specified type is redirected.

## Syntax

```
BOOL UnregisterPointerInputTarget(
  [in] HWND               hwnd,
  [in] POINTER_INPUT_TYPE pointerType
);
```

## Parameters

`[in] hwnd`

Window to be un-registered as a global redirection target on its desktop.

`[in] pointerType`

Type of pointer input to no longer be redirected to the specified window. This is any valid and supported value from the [POINTER\_INPUT\_TYPE](/en-us/windows/win32/api/winuser/ne-winuser-tagpointer_input_type)  enumeration. Note that the generic **PT\_POINTER** type and the **PT\_MOUSE** type are not valid in this parameter.

## Return value

If the function succeeds, the return value is non-zero.

If the function fails, the return value is zero. To get extended error information, call [GetLastError](/en-us/windows/desktop/api/errhandlingapi/nf-errhandlingapi-getlasterror).

## Remarks

An application that has successfully called the [RegisterPointerInputTarget](/en-us/windows/desktop/api/winuser/nf-winuser-registerpointerinputtarget) function can call this function to un-register the window from the role of global redirected target for the specified pointer type.

An application that has registered the same window as a global redirection target for multiple pointer input types can call the **UnregisterPointerInputTarget** to un-register the window for one of those types while leaving the window registered for the remaining types.

If the calling thread does not have the UI Access privilege, this function fails with the last error set to **ERROR\_ACCESS\_DENIED**.

If the specified pointer input type is not valid, this function fails with the last error set to **ERROR\_INVALID\_PARAMETER**.

If the calling thread does not own the specified window, this function fails with the last error set to **ERROR\_ACCESS\_DENIED**.

If the specified window is not the registered global redirection target for the specified pointer input type on its desktop, this function takes no action and returns success.

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
