# UiaGetReservedMixedAttributeValue

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/nf-uiautomationcoreapi-uiagetreservedmixedattributevalue)

# UiaGetReservedMixedAttributeValue function (uiautomationcoreapi.h)

Retrieves a reserved value indicating that the value of a Microsoft UI Automation text attribute varies within a text range.

## Syntax

```
HRESULT UiaGetReservedMixedAttributeValue(
  [out] IUnknown **punkMixedAttributeValue
);
```

## Parameters

`[out] punkMixedAttributeValue`

Type: **[IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown)\*\***

Receives
a reserved value specifying that
an attribute varies over a text range.
This parameter is passed uninitialized.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this function succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2003 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcoreapi.h |
| **Library** | Uiautomationcore.lib |
| **DLL** | Uiautomationcore.dll |

## See also

[Functions for Providers](/en-us/windows/desktop/WinAuto/uiauto-functions)

[Text and TextRange Control Patterns](/en-us/windows/desktop/WinAuto/uiauto-implementingtextandtextrange)

---
