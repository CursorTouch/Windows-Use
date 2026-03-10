# CreateStdAccessibleProxyA

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/oleacc/nf-oleacc-createstdaccessibleproxya)

# CreateStdAccessibleProxyA function (oleacc.h)

Creates an accessible object that has the properties and methods of the specified class of system-provided user interface element.

## Syntax

```
HRESULT CreateStdAccessibleProxyA(
  [in]  HWND   hwnd,
  [in]  LPCSTR pClassName,
  [in]  LONG   idObject,
  [in]  REFIID riid,
  [out] void   **ppvObject
);
```

## Parameters

`[in] hwnd`

Type: **[HWND](/en-us/windows/desktop/WinProg/windows-data-types)**

Window handle of the system-provided user interface element (a control) for which an accessible object is created.

`[in] pClassName`

Type: **[LPCTSTR](/en-us/windows/desktop/WinProg/windows-data-types)**

Pointer to a null-terminated string of the class name of a system-provided user interface element for which an accessible object is created. The window class name is one of the common controls (defined in Comctl32.dll), predefined controls (defined in User32.dll), or window elements.

`[in] idObject`

Type: **[LONG](/en-us/windows/desktop/WinProg/windows-data-types)**

Object ID. This value is usually [OBJID\_CLIENT](/en-us/windows/desktop/WinAuto/object-identifiers), which is one of the object identifier constants, but it may be another object identifier.

`[in] riid`

Type: **REFIID**

Reference identifier of the interface requested. This value is one of the following: IID\_IAccessible, IID\_IDispatch, IID\_IEnumVARIANT, or IID\_IUnknown.

`[out] ppvObject`

Type: **void\*\***

Address of a pointer variable that receives the address of the specified interface.

## Return value

Type: **STDAPI**

If successful, returns S\_OK.

If not successful, returns a standard [COM error code](/en-us/windows/desktop/WinAuto/return-values).

## Remarks

Server applications call this function when they contain a custom control that is similar to a system-provided control. Server applications can call **CreateStdAccessibleProxy** to override the [IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible) methods and properties as required to match their custom controls. Alternatively, server developers can use Dynamic Annotation to override specific properties without having to use difficult subclassing techniques that were required with **CreateStdAccessibleProxy**. Server developers should still use **CreateStdAccessibleProxy** for structural changes, such as hiding a child element or creating a placeholder child element. This approach saves server developers the work of fully implementing all of the **IAccessible** properties and methods.

This function is similar to [CreateStdAccessibleObject](/en-us/windows/desktop/api/oleacc/nf-oleacc-createstdaccessibleobject), except that **CreateStdAccessibleObject** always uses the class name associated with the *hwnd* whereas **CreateStdAccessibleProxy** allows you to specify the class name as a parameter.

Use **CreateStdAccessibleProxy** to create an accessible object for a user interface element that is superclassed. When a user interface element is superclassed, an application creates a custom control with a window class name different from the predefined control on which it is based. Because the class name associated with the *hwnd* parameter is the superclass window class name, specify the base class name (the system class name on which the superclassed control is based) in *pszClassName*.

Note

The oleacc.h header defines CreateStdAccessibleProxy as an alias that automatically selects the ANSI or Unicode version of this function based on the definition of the UNICODE preprocessor constant. Mixing usage of the encoding-neutral alias with code that is not encoding-neutral can lead to mismatches that result in compilation or runtime errors. For more information, see [Conventions for Function Prototypes](/en-us/windows/win32/intl/conventions-for-function-prototypes).

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

[Appendix A: Supported User Interface Elements Reference](/en-us/windows/desktop/WinAuto/appendix-a--supported-user-interface-elements-reference)

[CreateStdAccessibleObject](/en-us/windows/desktop/api/oleacc/nf-oleacc-createstdaccessibleobject)

[IDispatch](/en-us/windows/desktop/WinAuto/idispatch-interface)

[Shortcuts for Exposing Custom User Interface Elements](/en-us/windows/desktop/WinAuto/shortcuts-for-exposing-custom-user-interface-elements)

---
