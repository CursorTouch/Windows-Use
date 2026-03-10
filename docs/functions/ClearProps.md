# ClearProps

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/oleacc/nf-oleacc-iaccpropservices-clearprops)

# IAccPropServices::ClearProps method (oleacc.h)

Servers use **ClearProps** to restore default values to properties of accessible elements that they had previously annotated.

If servers know the **HWND** of the object they want to clear, they can use [IAccPropServices::ClearHwndProps](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccpropservices-clearhwndprops).

## Syntax

```
HRESULT ClearProps(
  [in] const BYTE       *pIDString,
  [in] DWORD            dwIDStringLen,
  [in] const MSAAPROPID *paProps,
  [in] int              cProps
);
```

## Parameters

`[in] pIDString`

Type: **const [BYTE](/en-us/windows/desktop/WinProg/windows-data-types)\***

Identify the accessible element that is to be un-annotated.

`[in] dwIDStringLen`

Type: **[DWORD](/en-us/windows/desktop/WinProg/windows-data-types)**

Length of *pIDString*.

`[in] paProps`

Type: **const MSAAPROPID\***

Specify an array of properties that is to be reset. These properties will revert to the default behavior they displayed before they were annotated.

`[in] cProps`

Type: **int**

Size of *paProps* array.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If successful, returns S\_OK, even if the specified properties were never annotated on the accessible object; clearing already cleared properties is considered a success.

Returns E\_INVALIDARG if any of the properties in the *paProps* array are not supported.

May return other error codes under exceptional error conditions such as low memory.

## Remarks

See the support section for a list of supported properties and their expected types.

Clearing the annotation for a property will cause any associated resources to be released. If a callback property server was used (see [SetPropServer](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccpropservices-setpropserver)), it will be released.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps only] |
| **Minimum supported server** | Windows Server 2003 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | oleacc.h (include OleAcc.h Include Initguid.h first.) |
| **DLL** | Oleacc.dll |
| **Redistributable** | Active Accessibility 2.0 RDK on Windows NT 4.0 with SP6 and later and Windows 98 |

---
