# UiaHPatternObjectFromVariant

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/nf-uiautomationcoreapi-uiahpatternobjectfromvariant)

# UiaHPatternObjectFromVariant function (uiautomationcoreapi.h)

**Note**  This function is deprecated. Client applications should use the Microsoft UI Automation Component Object Model (COM) interfaces instead.

Gets a control pattern object from a [VARIANT](/en-us/windows/desktop/WinAuto/variant-structure) type.

## Syntax

```
HRESULT UiaHPatternObjectFromVariant(
  [in]  VARIANT           *pvar,
  [out] HUIAPATTERNOBJECT *phobj
);
```

## Parameters

`[in] pvar`

Type: **[VARIANT](/en-us/windows/desktop/WinAuto/variant-structure)\***

The pattern.

`[out] phobj`

Type: **HUIAPATTERNOBJECT \***

The address of a variable that receives the control pattern object.
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
