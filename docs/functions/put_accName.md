# put_accName

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/oleacc/nf-oleacc-iaccessible-put_accname)

# IAccessible::put\_accName method (oleacc.h)

[[IAccessible::put\_accName](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccessible-put_accname) is no longer supported. ]

The [IAccessible::put\_accName](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccessible-put_accname) method is no longer supported. Client applications should use a control-specific workaround, such as the [SetWindowText](/en-us/windows/desktop/api/winuser/nf-winuser-setwindowtexta) function. Servers should return E\_NOTIMPL.

## Syntax

```
HRESULT put_accName(
  [in, optional] VARIANT varChild,
  [in]           BSTR    szName
);
```

## Parameters

`[in, optional] varChild`

Not supported.

`[in] szName`

Not supported.

## Return value

Not supported.

## Requirements

| Requirement | Value |
| --- | --- |
| **Target Platform** | Windows |
| **Header** | oleacc.h |
| **Library** | Oleacc.lib |
| **DLL** | Oleacc.dll |

## See also

[IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible)

---
