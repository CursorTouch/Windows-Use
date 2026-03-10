# UiaNodeRelease

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/nf-uiautomationcoreapi-uianoderelease)

# UiaNodeRelease function (uiautomationcoreapi.h)

**Note**  This function is deprecated. Client applications should use the Microsoft UI Automation Component Object Model (COM) interfaces instead.

Deletes a node from memory.

## Syntax

```
BOOL UiaNodeRelease(
  [in] HUIANODE hnode
);
```

## Parameters

`[in] hnode`

Type: **HUIANODE**

The node to be deleted.

## Return value

Type: **[BOOL](/en-us/windows/desktop/WinProg/windows-data-types)**

**TRUE** if the node was successfully deleted; otherwise **FALSE**.

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
