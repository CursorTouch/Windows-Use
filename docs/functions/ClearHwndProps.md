# ClearHwndProps

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/oleacc/nf-oleacc-iaccpropservices-clearhwndprops)

# IAccPropServices::ClearHwndProps method (oleacc.h)

This method wraps [SetPropValue](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccpropservices-setpropvalue), [SetPropServer](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccpropservices-setpropserver), and [ClearProps](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccpropservices-clearprops), and provides a convenient entry point for callers who are annotating **HWND**-based accessible elements.

## Syntax

```
HRESULT ClearHwndProps(
  [in] HWND             hwnd,
  [in] DWORD            idObject,
  [in] DWORD            idChild,
  [in] const MSAAPROPID *paProps,
  [in] int              cProps
);
```

## Parameters

`[in] hwnd`

Type: **[HWND](/en-us/windows/desktop/WinProg/windows-data-types)**

Identifies the accessible element that is to be annotated. This replaces the identity string.

`[in] idObject`

Type: **[DWORD](/en-us/windows/desktop/WinProg/windows-data-types)**

Identifies the accessible element that is to be annotated. This replaces the identity string.

`[in] idChild`

Type: **[DWORD](/en-us/windows/desktop/WinProg/windows-data-types)**

Identifies the accessible element that is to be annotated. This replaces the identity string.

`[in] paProps`

Type: **const MSAAPROPID\***

Specifies an array of properties that is to be reset. These properties will revert to the default behavior that they displayed before they were annotated.

`[in] cProps`

Type: **int**

Specifies the number of properties in the *paProps* array.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If successful, returns S\_OK, even if the specified properties were never annotated on the accessible object; clearing already-cleared properties is considered a success.

Returns E\_INVALIDARG if any of the properties in the *paProps* array are not supported.

May return other error codes under exceptional error conditions such as low memory.

For descriptions of return values, see the corresponding [SetPropValue](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccpropservices-setpropvalue), [SetPropServer](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccpropservices-setpropserver), or [ClearProps](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccpropservices-clearprops) method.

## Remarks

By using this method, the caller does not have to obtain an identity string; it can specify the *hwnd*, *idObject*, and *idChild* parameters directly.

Additionally, [SetHwndPropStr](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccpropservices-sethwndpropstr) takes a regular Unicode string as a parameter; the caller does not need to specially allocate a **BSTR**.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps only] |
| **Minimum supported server** | Windows Server 2003 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | oleacc.h (include OleAcc.h Include Initguid.h first.) |
| **DLL** | Oleacc.dll |
| **Redistributable** | Active Accessibility 2.0 RDK on Windows NT 4.0 with SP6 and later and Windows 98 |

## See also

[ClearProps](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccpropservices-clearprops)

[IAccPropServices](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccpropservices)

[SetHwndProp](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccpropservices-sethwndprop)

[SetHwndPropServer](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccpropservices-sethwndpropserver)

[SetHwndPropStr](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccpropservices-sethwndpropstr)

---
