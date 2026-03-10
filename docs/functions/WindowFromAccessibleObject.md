# WindowFromAccessibleObject

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/oleacc/nf-oleacc-windowfromaccessibleobject)

# WindowFromAccessibleObject function (oleacc.h)

Retrieves the window handle that corresponds to a particular instance of an [IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible) interface.

## Syntax

```
HRESULT WindowFromAccessibleObject(
  [in]  IAccessible *unnamedParam1,
  [out] HWND        *phwnd
);
```

## Parameters

`[in] unnamedParam1`

Type: **IAccessible\***

Pointer to the [IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible) interface whose corresponding window handle will be retrieved. This parameter must not be **NULL**.

`[out] phwnd`

Type: **[HWND](/en-us/windows/desktop/WinProg/windows-data-types)\***

Address of a variable that receives a handle to the window containing the object specified in *pacc*. If this value is **NULL** after the call, the object is not contained within a window; for example, the mouse pointer is not contained within a window.

## Return value

Type: **STDAPI**

If successful, returns S\_OK.

If not successful, returns the following or another standard [COM error code](/en-us/windows/desktop/WinAuto/return-values).

| Return code | Description |
| --- | --- |
| **E\_INVALIDARG** | An argument is not valid. |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 2000 Professional [desktop apps only] |
| **Minimum supported server** | Windows Server 2003 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | oleacc.h |
| **Library** | Oleacc.lib |
| **DLL** | Oleacc.dll |
| **Redistributable** | Active Accessibility 1.3 RDK on Windows NT 4.0 with SP6 and later and Windows 95 |

## See also

[AccessibleObjectFromWindow](/en-us/windows/desktop/api/oleacc/nf-oleacc-accessibleobjectfromwindow)

[IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible)

---
