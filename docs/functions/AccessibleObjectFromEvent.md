# AccessibleObjectFromEvent

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/oleacc/nf-oleacc-accessibleobjectfromevent)

# AccessibleObjectFromEvent function (oleacc.h)

Retrieves the address of the [IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible) interface for the object that generated the event that is currently being processed by the client's event hook function.

## Syntax

```
HRESULT AccessibleObjectFromEvent(
  [in]  HWND        hwnd,
  [in]  DWORD       dwId,
  [in]  DWORD       dwChildId,
  [out] IAccessible **ppacc,
  [out] VARIANT     *pvarChild
);
```

## Parameters

`[in] hwnd`

Type: **[HWND](/en-us/windows/desktop/WinProg/windows-data-types)**

Specifies the window handle of the window that generated the event. This value must be the window handle that is sent to the event hook function.

`[in] dwId`

Type: **[DWORD](/en-us/windows/desktop/WinProg/windows-data-types)**

Specifies the object ID of the object that generated the event. This value must be the object ID that is sent to the event hook function.

`[in] dwChildId`

Type: **[DWORD](/en-us/windows/desktop/WinProg/windows-data-types)**

Specifies whether the event was triggered by an object or one of its child elements. If the object triggered the event, *dwChildID* is CHILDID\_SELF. If a child element triggered the event, *dwChildID* is the element's child ID. This value must be the child ID that is sent to the event hook function.

`[out] ppacc`

Type: **IAccessible\*\***

Address of a pointer variable that receives the address of an [IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible) interface. The interface is either for the object that generated the event, or for the parent of the element that generated the event.

`[out] pvarChild`

Type: **VARIANT\***

Address of a [VARIANT structure](/en-us/windows/desktop/WinAuto/variant-structure) that specifies the child ID that can be used to access information about the UI element.

## Return value

Type: **STDAPI**

If successful, returns S\_OK.

If not successful, returns one of the following or another standard [COM error code](/en-us/windows/desktop/WinAuto/return-values).

| Return code | Description |
| --- | --- |
| **E\_INVALIDARG** | An argument is not valid. |

## Remarks

Clients call this function within an event hook function to obtain an [IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible) interface pointer to either the object that generated the event or to the parent of the element that generated the event. The parameters sent to the [WinEventProc](/en-us/windows/desktop/api/winuser/nc-winuser-wineventproc) callback function must be used for this function's *hwnd*, *dwObjectID*, and *dwChildID* parameters.

This function retrieves the lowest-level accessible object in the object hierarchy that is associated with an event. If the element that generated the event is not an accessible object (that is, does not support [IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible)), then the function retrieves the **IAccessible** interface of the parent object. The parent object must provide information about the child element through the **IAccessible** interface.

As with other [IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible) methods and functions, clients might receive errors for **IAccessible** interface pointers because of a user action. For more information, see [Receiving Errors for IAccessible Interface Pointers](/en-us/windows/desktop/WinAuto/receiving-errors-for-iaccessible-interface-pointers).

This function fails if called in response to [EVENT\_OBJECT\_CREATE](/en-us/windows/desktop/WinAuto/event-constants) because the object is not fully initialized. Similarly, clients should not call this in response to [EVENT\_OBJECT\_DESTROY](/en-us/windows/desktop/WinAuto/event-constants) because the object is no longer available and cannot respond. Clients watch for [EVENT\_OBJECT\_SHOW](/en-us/windows/desktop/WinAuto/event-constants) and [EVENT\_OBJECT\_HIDE](/en-us/windows/desktop/WinAuto/event-constants) events rather than for **EVENT\_OBJECT\_CREATE** and **EVENT\_OBJECT\_DESTROY**.

#### Examples

The following example code shows this method being called in a [WinEventProc](/en-us/windows/desktop/api/winuser/nc-winuser-wineventproc) event handler.

```
void CALLBACK HandleWinEvent(HWINEVENTHOOK hook, DWORD event, HWND hwnd, 
                             LONG idObject, LONG idChild, 
                             DWORD dwEventThread, DWORD dwmsEventTime)
{
    IAccessible* pAcc = NULL;
    VARIANT varChild;
    HRESULT hr = AccessibleObjectFromEvent(hwnd, idObject, idChild, &pAcc, &varChild);  
    if ((hr == S_OK) && (pAcc != NULL))
    {
        // Do something with the accessible object, then release it.        
        // ... 
        pAcc->Release();
    }
}
```

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

[AccessibleObjectFromPoint](/en-us/windows/desktop/api/oleacc/nf-oleacc-accessibleobjectfrompoint)

[AccessibleObjectFromWindow](/en-us/windows/desktop/api/oleacc/nf-oleacc-accessibleobjectfromwindow)

[IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible)

[VARIANT](/en-us/windows/desktop/WinAuto/variant-structure)

[WinEventProc](/en-us/windows/desktop/api/winuser/nc-winuser-wineventproc)

---
