# UiaHUiaNodeFromVariant

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/nf-uiautomationcoreapi-uiahuianodefromvariant)

# UiaHUiaNodeFromVariant function (uiautomationcoreapi.h)

**Note**  This function is deprecated. Client applications should use the Microsoft UI Automation Component Object Model (COM) interfaces instead.

Gets an HUIANODE from a [VARIANT](/en-us/windows/desktop/WinAuto/variant-structure) type.

## Syntax

```
HRESULT UiaHUiaNodeFromVariant(
  [in]  VARIANT  *pvar,
  [out] HUIANODE *phnode
);
```

## Parameters

`[in] pvar`

Type: **[VARIANT](/en-us/windows/desktop/WinAuto/variant-structure)\***

The node.

`[out] phnode`

Type: **HUIANODE\***

The address of a variable that receives the HUIANODE.
This parameter is passed uninitialized.

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
