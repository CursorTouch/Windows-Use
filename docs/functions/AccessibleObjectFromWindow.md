# AccessibleObjectFromWindow

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/oleacc/nf-oleacc-accessibleobjectfromwindow)

# AccessibleObjectFromWindow function (oleacc.h)

Retrieves the address of the specified interface for the object associated with the specified window.

## Syntax

```
HRESULT AccessibleObjectFromWindow(
  [in]  HWND   hwnd,
  [in]  DWORD  dwId,
  [in]  REFIID riid,
  [out] void   **ppvObject
);
```

## Parameters

`[in] hwnd`

Type: **[HWND](/en-us/windows/desktop/WinProg/windows-data-types)**

Specifies the handle of a window for which an object is to be retrieved. To retrieve an interface pointer to the cursor or caret object, specify **NULL** and use the appropriate object ID in *dwObjectID*.

`[in] dwId`

Type: **[DWORD](/en-us/windows/desktop/WinProg/windows-data-types)**

Specifies the object ID. This value is one of the standard [object identifier](/en-us/windows/desktop/WinAuto/object-identifiers) constants or a custom object ID such as [OBJID\_NATIVEOM](/en-us/windows/desktop/WinAuto/object-identifiers), which is the object ID for the Office native object model. For more information about **OBJID\_NATIVEOM**, see the Remarks section in this topic.

`[in] riid`

Type: **REFIID**

Specifies the reference identifier of the requested interface. This value is either IID\_IAccessible or IID\_IDispatch, but it can also be IID\_IUnknown, or the IID of any interface that the object is expected to support.

`[out] ppvObject`

Type: **void\*\***

Address of a pointer variable that receives the address of the specified interface.

## Return value

Type: **STDAPI**

If successful, returns S\_OK.

If not successful, returns one of the following or another standard [COM error code](/en-us/windows/desktop/WinAuto/return-values).

| Return code | Description |
| --- | --- |
| **E\_INVALIDARG** | An argument is not valid. |
| **E\_NOINTERFACE** | The requested interface is not supported. |

## Remarks

Clients call this function to retrieve the address of an object's [IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible), [IDispatch](/en-us/windows/desktop/WinAuto/idispatch-interface), [IEnumVARIANT](/en-us/windows/win32/api/oaidl/nn-oaidl-ienumvariant), [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown), or other supported interface pointer.

As with other [IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible) methods and functions, clients might receive errors for **IAccessible** interface pointers because of a user action. For more information, see [Receiving Errors for IAccessible Interface Pointers](/en-us/windows/desktop/WinAuto/receiving-errors-for-iaccessible-interface-pointers).

Clients use this function to obtain access to the Microsoft Office 2000 native object model. The native object model provides clients with accessibility information about an Office application's document or client area that is not exposed by Microsoft Active Accessibility.

To obtain an [IDispatch](/en-us/windows/desktop/WinAuto/idispatch-interface) interface pointer to a class supported by the native object model, specify [OBJID\_NATIVEOM](/en-us/windows/desktop/WinAuto/object-identifiers) in *dwObjectID*. When using this object identifier, the *hwnd* parameter must match the following window class types.

| Office application | Window class | IDispatch pointer to |
| --- | --- | --- |
| Word | \_WwG | Window |
| Excel | EXCEL7 | Window |
| PowerPoint | paneClassDC | DocumentWindow |
| Command Bars | MsoCommandBar | CommandBar |

Note that the above window classes correspond to the innermost document window or pane window. For more information about the Office object model, see the [Microsoft Office 2000/Visual Basic Programmer's Guide](/en-us/previous-versions/office/developer/office2000/aa141393(v=office.10)).

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

[AccessibleObjectFromEvent](/en-us/windows/desktop/api/oleacc/nf-oleacc-accessibleobjectfromevent)

[AccessibleObjectFromPoint](/en-us/windows/desktop/api/oleacc/nf-oleacc-accessibleobjectfrompoint)

[IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible)

[IDispatch](/en-us/windows/desktop/WinAuto/idispatch-interface)

---
