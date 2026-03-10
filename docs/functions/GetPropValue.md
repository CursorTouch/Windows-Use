# GetPropValue

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/oleacc/nf-oleacc-iaccpropserver-getpropvalue)

# IAccPropServer::GetPropValue method (oleacc.h)

Retrieves a property value for an accessible element.

## Syntax

```
HRESULT GetPropValue(
  [in]  const BYTE *pIDString,
  [in]  DWORD      dwIDStringLen,
  [in]  MSAAPROPID idProp,
  [out] VARIANT    *pvarValue,
  [out] BOOL       *pfHasProp
);
```

## Parameters

`[in] pIDString`

Type: **const BYTE\***

Contains a string that identifies the property being requested.

`[in] dwIDStringLen`

Type: **[DWORD](/en-us/windows/desktop/WinProg/windows-data-types)**

Specifies the length of the identity string specified by the *pIDString* parameter.

`[in] idProp`

Type: **MSAAPROPID**

Specifies a GUID indicating the desired property.

`[out] pvarValue`

Type: **VARIANT\***

Specifies the value of the overridden property. This parameter is valid only if *pfHasProp* is **TRUE**. The server must set this to VT\_EMPTY if *pfHasProp* is set to **FALSE**.

`[out] pfHasProp`

Type: **[BOOL](/en-us/windows/desktop/WinProg/windows-data-types)\***

Indicates whether the server is supplying a value for the requested property. The server should set this to **TRUE** if it is returning an overriding property or to **FALSE** if it is not returning a property (in which case it should also set *pvarValue* to VT\_EMPTY).

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

Return S\_OK, except under exceptional error conditions such as low memory. If the specified property is not overridden, then *pfHasProp* should be set to **FALSE** and *pvarValue* should be set to VT\_EMPTY by the server.

## Remarks

If a single callback object is registered for annotating multiple accessible elements, the identity string can be used to determine which element this request refers to.

If the accessible element is **HWND**-based, [IAccPropServices::DecomposeHwndIdentityString](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccpropservices-decomposehwndidentitystring) can be used to extract the HWND/idObject/idChild from the identity string.

If the callback has a value to return for the specified property, it should return it in *pvarValue* and set *pfHasProp* to **TRUE**. Otherwise it should set *pvarValue* to VT\_EMPTY and set *pfHasProp* to **FALSE**. In this latter case, the original [IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible) interface pointer will be used to obtain a value for this property.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows Vista or Windows XP |
| **Minimum supported server** | Windows Server 2003 |
| **Target Platform** | Windows |
| **Header** | oleacc.h (include OleAcc.h Include Initguid.h first.) |
| **DLL** | Oleacc.dll |
| **Redistributable** | Active Accessibility 2.0 RDK on Windows NT 4.0 with SP6 and later and Windows 98 |

---
