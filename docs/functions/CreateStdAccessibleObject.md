# CreateStdAccessibleObject

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/oleacc/nf-oleacc-createstdaccessibleobject)

# CreateStdAccessibleObject function (oleacc.h)

Creates an accessible object with the methods and properties of the specified type of system-provided user interface element.

## Syntax

```
HRESULT CreateStdAccessibleObject(
  [in]  HWND   hwnd,
  [in]  LONG   idObject,
  [in]  REFIID riid,
  [out] void   **ppvObject
);
```

## Parameters

`[in] hwnd`

Type: **[HWND](/en-us/windows/desktop/WinProg/windows-data-types)**

Window handle of the system-provided user interface element (a control) for which an accessible object is created.

`[in] idObject`

Type: **[LONG](/en-us/windows/desktop/WinProg/windows-data-types)**

Object ID. This value is usually [OBJID\_CLIENT](/en-us/windows/desktop/WinAuto/object-identifiers), but it may be another object identifier.

`[in] riid`

Type: **REFIID**

Reference identifier of the requested interface. This value is one of the following: IID\_IAccessible, IID\_IDispatch, IID\_IEnumVARIANT, or IID\_IUnknown.

`[out] ppvObject`

Type: **void\*\***

Address of a pointer variable that receives the address of the specified interface.

## Return value

Type: **STDAPI**

If successful, returns S\_OK.

If not successful, returns a standard [COM error code](/en-us/windows/desktop/WinAuto/return-values).

## Remarks

Server applications call this function when they contain a custom UI object that is similar to a system-provided object. Server developers can call **CreateStdAccessibleObject** to override the [IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible) methods and properties as required to match their custom objects. Alternatively, server developers can use Dynamic Annotation to override specific properties without having to use difficult subclassing techniques that **CreateStdAccessibleObject** requires. Server developers should still use **CreateStdAccessibleObject** for structural changes, such as hiding a child element or creating a placeholder child element. This approach saves server developers the work of fully implementing all of the **IAccessible** properties and methods.

This function is similar to [CreateStdAccessibleProxy](/en-us/windows/desktop/api/oleacc/nf-oleacc-createstdaccessibleproxya), except that **CreateStdAccessibleProxy** allows you to specify the class name as a parameter whereas **CreateStdAccessibleObject** uses the class name associated with the *hwnd* parameter.

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

[CreateStdAccessibleProxy](/en-us/windows/desktop/api/oleacc/nf-oleacc-createstdaccessibleproxya)

[IDispatch](/en-us/windows/desktop/WinAuto/idispatch-interface)

[Shortcuts for Exposing Custom User Interface Elements](/en-us/windows/desktop/WinAuto/shortcuts-for-exposing-custom-user-interface-elements)

---
