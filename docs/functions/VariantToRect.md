# VariantToRect

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomation-varianttorect)

# IUIAutomation::VariantToRect method (uiautomationclient.h)

Converts a [VARIANT](/en-us/windows/desktop/api/oaidl/ns-oaidl-variant) containing rectangle coordinates to a [RECT](/en-us/windows/desktop/api/windef/ns-windef-rect).

## Syntax

```
HRESULT VariantToRect(
  [in]          VARIANT var,
  [out, retval] RECT    *rc
);
```

## Parameters

`[in] var`

Type: **[VARIANT](/en-us/windows/desktop/api/oaidl/ns-oaidl-variant)**

The coordinates of a rectangle.

`[out, retval] rc`

Type: **[RECT](/en-us/windows/desktop/api/windef/ns-windef-rect)\***

Receives the converted rectangle coordinates.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

---
