# AccessibleObjectFromID

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/oleacc/nf-oleacc-iaccessiblehandler-accessibleobjectfromid)

# IAccessibleHandler::AccessibleObjectFromID method (oleacc.h)

The **AccessibleObjectFromID** method retrieves an [IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible) interface pointer for the interface associated with the given object ID. Oleacc.dll uses this method to obtain an **IAccessible** interface pointer for proxies that are supplied by other code.

**Note**  **IAccessibleHandler::AccessibleObjectFromID** is deprecated and should not be used.

## Syntax

```
HRESULT AccessibleObjectFromID(
  [in]  long         hwnd,
  [in]  long         lObjectID,
  [out] LPACCESSIBLE *pIAccessible
);
```

## Parameters

`[in] hwnd`

Type: **long**

Specifies the handle of a window for which an [IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible) interface pointer is to be retrieved.

`[in] lObjectID`

Type: **long**

Specifies the object ID. This value is one of the standard [object identifier](/en-us/windows/desktop/WinAuto/object-identifiers) constants or a custom object ID.

`[out] pIAccessible`

Type: **LPACCESSIBLE\***

Specifies the address of a pointer variable that receives the address of the object's [IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible) interface.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If successful, returns S\_OK.

If not successful, returns one of the following or another standard [COM error code](/en-us/windows/desktop/WinAuto/return-values).

| Error | Description |
| --- | --- |
| **E\_INVALIDARG** | An argument is not valid. |
| **E\_NOINTERFACE** | The requested interface is not supported. |

## Remarks

Oleacc calls this function to obtain an [IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible) interface pointer for **HWND**s that have the class name that this handler is registered for.

At startup, Oleacc looks in the registry key HKLM\SOFTWARE\Microsoft\Active Accessibility\Handlers and enumerates over each subkey (Oleacc expects the subkey to be a GUID). Oleacc reads the associated class name from HKCR\CLSID{guid}\AccClassName, where {guid} was the GUID found under the HKLM\SOFTWARE\Microsoft\Active Accessibility\Handlers key. When Oleacc finds a window with a class name that matches the GUID, it CoCreates the object using the GUID, retrieves the [IAccessibleHandler](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessiblehandler) interface pointer, and calls **AccessibleObjectFromID** on it to get at [IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible) interface pointer.

As with other [IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible) methods and functions, clients might receive errors for **IAccessible** interface pointers because of a user action. For more information, see [Receiving Errors for IAccessible Interface Pointers](/en-us/windows/desktop/WinAuto/receiving-errors-for-iaccessible-interface-pointers).

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

---
