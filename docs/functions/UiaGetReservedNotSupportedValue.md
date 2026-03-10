# UiaGetReservedNotSupportedValue

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/nf-uiautomationcoreapi-uiagetreservednotsupportedvalue)

# UiaGetReservedNotSupportedValue function (uiautomationcoreapi.h)

Retrieves a reserved value indicating that a Microsoft UI Automation property or a text attribute is not supported.

## Syntax

```
HRESULT UiaGetReservedNotSupportedValue(
  [out] IUnknown **punkNotSupportedValue
);
```

## Parameters

`[out] punkNotSupportedValue`

Type: **[IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown)\*\***

Receives the object representing the value.
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
