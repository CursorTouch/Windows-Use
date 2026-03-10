# RectToVariant

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomation-recttovariant)

# IUIAutomation::RectToVariant method (uiautomationclient.h)

Creates a [VARIANT](/en-us/windows/desktop/WinAuto/variant-structure) that contains the coordinates of a rectangle.

## Syntax

```
HRESULT RectToVariant(
  [in]          RECT    rc,
  [out, retval] VARIANT *var
);
```

## Parameters

`[in] rc`

Type: **[RECT](/en-us/windows/desktop/api/windef/ns-windef-rect)\***

A pointer to a structure that contains the coordinates of the rectangle.

`[out, retval] var`

Type: **[VARIANT](/en-us/windows/desktop/api/oaidl/ns-oaidl-variant)\***

Receives the coordinates of the rectangle.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

The returned [VARIANT](/en-us/windows/desktop/WinAuto/variant-structure) has a data type of VT\_ARRAY | VT\_R8.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[IUIAutomation](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomation)

[IUIAutomation::VariantToRect](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomation-varianttorect)

---
