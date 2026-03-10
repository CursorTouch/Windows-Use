# UiaClientsAreListening

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/nf-uiautomationcoreapi-uiaclientsarelistening)

# UiaClientsAreListening function (uiautomationcoreapi.h)

Gets a value that indicates whether any client application is subscribed to Microsoft UI Automation events.

## Syntax

```
BOOL UiaClientsAreListening();
```

## Return value

Type: **[BOOL](/en-us/windows/desktop/WinProg/windows-data-types)**

**TRUE** if a client has subscribed to events; otherwise **FALSE**.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2003 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcoreapi.h |
| **Library** | Uiautomationcore.lib |
| **DLL** | Uiautomationcore.dll |

---
