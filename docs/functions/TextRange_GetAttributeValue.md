# TextRange_GetAttributeValue

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/nf-uiautomationcoreapi-textrange_getattributevalue)

# TextRange\_GetAttributeValue function (uiautomationcoreapi.h)

**Note**  This function is deprecated. Client applications should use the Microsoft UI Automation Component Object Model (COM) interfaces instead.

Gets the value of a text attribute for a text range.

## Syntax

```
HRESULT TextRange_GetAttributeValue(
  [in]  HUIATEXTRANGE   hobj,
  [in]  TEXTATTRIBUTEID attributeId,
  [out] VARIANT         *pRetVal
);
```

## Parameters

`[in] hobj`

Type: **HUIATEXTRANGE**

A text range object.

`[in] attributeId`

Type: **TEXTATTRIBUTEID**

The text attribute whose value is wanted. For a list of text attribute IDs, see [Text Attribute Identifiers](/en-us/windows/desktop/WinAuto/uiauto-textattribute-ids).

`[out] pRetVal`

Type: **[VARIANT](/en-us/windows/desktop/WinAuto/variant-structure)\***

When this function returns, contains
the value of the attribute for the text range.
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
