# UiaGetRuntimeId

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/nf-uiautomationcoreapi-uiagetruntimeid)

# UiaGetRuntimeId function (uiautomationcoreapi.h)

**Note**  This function is deprecated. Client applications should use the Microsoft UI Automation Component Object Model (COM) interfaces instead.

Retrieves the runtime identifier of a UI Automation node.

## Syntax

```
HRESULT UiaGetRuntimeId(
  [in]  HUIANODE  hnode,
  [out] SAFEARRAY **pruntimeId
);
```

## Parameters

`[in] hnode`

Type: **HUIANODE**

The node for which the identifier is being requested.

`[out] pruntimeId`

Type: **[SAFEARRAY](/en-us/windows/win32/api/oaidl/ns-oaidl-safearray)\*\***

The address of a variable that receives a pointer to a [SAFEARRAY](/en-us/windows/win32/api/oaidl/ns-oaidl-safearray) that contains the runtime identifier of the type VT\_I4. This parameter is passed uninitialized.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

Returns S\_OK if successful or an error value otherwise.

## Remarks

The runtime identifier should be treated as an opaque value and used only for comparison.

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
