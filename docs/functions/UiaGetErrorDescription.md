# UiaGetErrorDescription

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/nf-uiautomationcoreapi-uiageterrordescription)

# UiaGetErrorDescription function (uiautomationcoreapi.h)

**Note**  This function is deprecated. Client applications should use the Microsoft UI Automation Component Object Model (COM) interfaces instead.

Gets an error string so that it can be passed to the client.
This method is not used directly by clients.

## Syntax

```
BOOL UiaGetErrorDescription(
  [out] BSTR *pDescription
);
```

## Parameters

`[out] pDescription`

Type: **BSTR\***

The address of a variable that receives the description of the error. This parameter is passed uninitialized.

## Return value

Type: **[BOOL](/en-us/windows/desktop/WinProg/windows-data-types)**

**TRUE** if an error description can be reported; otherwise **FALSE**.

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
