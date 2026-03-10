# UiaGetPatternProvider

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/nf-uiautomationcoreapi-uiagetpatternprovider)

# UiaGetPatternProvider function (uiautomationcoreapi.h)

**Note**  This function is deprecated. Client applications should use the Microsoft UI Automation Component Object Model (COM) interfaces instead.

Retrieves a *control pattern*.

## Syntax

```
HRESULT UiaGetPatternProvider(
  [in]  HUIANODE          hnode,
  [in]  PATTERNID         patternId,
  [out] HUIAPATTERNOBJECT *phobj
);
```

## Parameters

`[in] hnode`

Type: **HUIANODE**

The element that implements the pattern.

`[in] patternId`

Type: **PATTERNID**

The identifier of the control pattern being requested. For a list of control pattern IDs, see [Control Pattern Identifiers](/en-us/windows/desktop/WinAuto/uiauto-controlpattern-ids).

`[out] phobj`

Type: **HPATTERNOBJECT\***

The address of a variable that receives a handle to the control pattern.
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
