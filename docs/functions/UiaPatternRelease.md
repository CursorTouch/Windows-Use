# UiaPatternRelease

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/nf-uiautomationcoreapi-uiapatternrelease)

# UiaPatternRelease function (uiautomationcoreapi.h)

**Note**  This function is deprecated. Client applications should use the Microsoft UI Automation Component Object Model (COM) interfaces instead.

Deletes an allocated pattern object from memory.

## Syntax

```
BOOL UiaPatternRelease(
  [in] HUIAPATTERNOBJECT hobj
);
```

## Parameters

`[in] hobj`

Type: **HUIAPATTERNOBJECT**

The pattern object to be deleted.

## Return value

Type: **[BOOL](/en-us/windows/desktop/WinProg/windows-data-types)**

**TRUE** if the pattern was successfully deleted; otherwise **FALSE**.

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
