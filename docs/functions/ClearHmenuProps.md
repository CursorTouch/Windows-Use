# ClearHmenuProps

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/oleacc/nf-oleacc-iaccpropservices-clearhmenuprops)

# IAccPropServices::ClearHmenuProps method (oleacc.h)

This method wraps [ClearProps](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccpropservices-clearprops), and provides a convenient entry point for callers who are annotating **HMENU**-based accessible elements.

## Syntax

```
HRESULT ClearHmenuProps(
  [in] HMENU            hmenu,
  [in] DWORD            idChild,
  [in] const MSAAPROPID *paProps,
  [in] int              cProps
);
```

## Parameters

`[in] hmenu`

Type: **[HMENU](/en-us/windows/desktop/WinProg/windows-data-types)**

Identifies the **HMENU**-based accessible element to be annotated.

`[in] idChild`

Type: **[DWORD](/en-us/windows/desktop/WinProg/windows-data-types)**

Specifies the child ID of the accessible element.

`[in] paProps`

Type: **const MSAAPROPID\***

Specifies an array of properties to be reset. These properties will revert to the default behavior that they displayed before they were annotated.

`[in] cProps`

Type: **int**

Specifies the number of properties in the *paProps* array.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If successful, returns S\_OK, even if the specified properties were never annotated on the accessible object; clearing already-cleared properties is considered a success.

Returns E\_INVALIDARG if any of the properties in the *paProps* array are not supported.

May return other error codes under exceptional error conditions such as low memory.

For descriptions of other parameters and return values, see the [ClearProps](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccpropservices-clearprops) method.

## Remarks

By using this method, the caller does not have to obtain an identity string; it can specify the *hmenu* and *idChild* parameters directly.

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

[SetHmenuProp](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccpropservices-sethmenuprop)

[SetHmenuPropServer](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccpropservices-sethmenupropserver)

[SetHmenuPropStr](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccpropservices-sethmenupropstr)

---
