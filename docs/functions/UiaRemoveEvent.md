# UiaRemoveEvent

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/nf-uiautomationcoreapi-uiaremoveevent)

# UiaRemoveEvent function (uiautomationcoreapi.h)

**Note**  This function is deprecated. Client applications should use the Microsoft UI Automation Component Object Model (COM) interfaces instead.

Removes a listener for events on a node in the UI Automation tree.

## Syntax

```
HRESULT UiaRemoveEvent(
  [in] HUIAEVENT hEvent
);
```

## Parameters

`[in] hEvent`

Type: **HUIAEVENT**

The event to remove. This value was retrieved from [UiaAddEvent](/en-us/windows/desktop/api/uiautomationcoreapi/nf-uiautomationcoreapi-uiaaddevent).

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

Returns S\_OK if successful or an error value otherwise.

## Remarks

The callback pointer, the scope, the node, and the list of properties must match exactly the parameters that were sent to the
corresponding [UiaAddEvent](/en-us/windows/desktop/api/uiautomationcoreapi/nf-uiautomationcoreapi-uiaaddevent).

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
