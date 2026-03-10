# GetParentAccessible

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/oleacc/nf-oleacc-iaccessiblewindowlesssite-getparentaccessible)

# IAccessibleWindowlessSite::GetParentAccessible method (oleacc.h)

Retrieves an [IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible) pointer for the parent of a windowless Microsoft ActiveX control in the accessibility tree.

## Syntax

```
HRESULT GetParentAccessible(
  [out, optional] IAccessible **ppParent
);
```

## Parameters

`[out, optional] ppParent`

Type: **[IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible)\*\***

Receives the [IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible) pointer for the parent of the windowless ActiveX control.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

To return its parent [IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible) object, an object that implements **IAccessible** must be able to implement the [get\_accParent](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccessible-get_accparent) method. Implementing **get\_accParent** is difficult for a windowless ActiveX control because the control might be unable to determine its location in the accessible tree of the parent object. The **GetParentAccessible** method enables a windowless ActiveX control to query its site for the parent object, and then return the parent object to the client that called **get\_accParent**.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 8 [desktop apps only] |
| **Minimum supported server** | Windows Server 2012 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | oleacc.h |
| **Library** | Oleacc.lib |
| **DLL** | Oleacc.dll |

## See also

[IAccessibleWindowlessSite](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessiblewindowlesssite)

---
