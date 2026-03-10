# TextRange_FindAttribute

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/nf-uiautomationcoreapi-textrange_findattribute)

# TextRange\_FindAttribute function (uiautomationcoreapi.h)

**Note**  This function is deprecated. Client applications should use the Microsoft UI Automation Component Object Model (COM) interfaces instead.

Searches in a specified direction for the first piece of text supporting a specified text attribute.

## Syntax

```
HRESULT TextRange_FindAttribute(
  [in]  HUIATEXTRANGE   hobj,
  [in]  TEXTATTRIBUTEID attributeId,
  [in]  VARIANT         val,
  [in]  BOOL            backward,
  [out] HUIATEXTRANGE   *pRetVal
);
```

## Parameters

`[in] hobj`

Type: **HUIATEXTRANGE**

The text range to search.

`[in] attributeId`

Type: **TEXTATTRIBUTEID**

The text attribute to search for. For a list of text attribute IDs, see [Text Attribute Identifiers](/en-us/windows/desktop/WinAuto/uiauto-textattribute-ids).

`[in] val`

Type: **[VARIANT](/en-us/windows/desktop/WinAuto/variant-structure)**

The value of the attribute that the client wants to find.

`[in] backward`

Type: **[BOOL](/en-us/windows/desktop/WinProg/windows-data-types)**

**TRUE** to search backward, otherwise **FALSE**.

`[out] pRetVal`

Type: **HUITEXTRANGE\***

When this function returns, contains
the first matching text range.
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
