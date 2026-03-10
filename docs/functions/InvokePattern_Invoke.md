# InvokePattern_Invoke

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/nf-uiautomationcoreapi-invokepattern_invoke)

# InvokePattern\_Invoke function (uiautomationcoreapi.h)

**Note**  This function is deprecated. Client applications should use the Microsoft UI Automation Component Object Model (COM) interfaces instead.

Sends a request to activate a control and initiate its single, unambiguous action.

## Syntax

```
HRESULT InvokePattern_Invoke(
  [in] HUIAPATTERNOBJECT hobj
);
```

## Parameters

`[in] hobj`

Type: **HUIAPATTERNOBJECT**

The *control pattern* object.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

Returns S\_OK if successful or an error value otherwise.

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
