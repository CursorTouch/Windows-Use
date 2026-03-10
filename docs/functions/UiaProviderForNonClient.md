# UiaProviderForNonClient

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/nf-uiautomationcoreapi-uiaproviderfornonclient)

# UiaProviderForNonClient function (uiautomationcoreapi.h)

Gets the provider for the entire non-client area of a window, or for a control in the non-client area of a window.

## Syntax

```
HRESULT UiaProviderForNonClient(
  [in]  HWND                      hwnd,
  [in]  long                      idObject,
  [in]  long                      idChild,
  [out] IRawElementProviderSimple **ppProvider
);
```

## Parameters

`[in] hwnd`

Type: **[HWND](/en-us/windows/desktop/WinProg/windows-data-types)**

The window that owns the non-client area or non-client control.

`[in] idObject`

Type: **long**

The object identifier of the non-client control, or [OBJID\_WINDOW](/en-us/windows/desktop/WinAuto/object-identifiers) for the entire non-client area. For a list of possible values, see **Object Identifiers**.

`[in] idChild`

Type: **long**

The child identifier of the non-client control.

`[out] ppProvider`

Type: **[IRawElementProviderSimple](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-irawelementprovidersimple)\*\***

Receives the provider for the non-client area or non-client control.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

Returns S\_OK if successful or an error value otherwise.

## Remarks

This function returns the default Microsoft UI Automation provider for the non-client area of a window. UI Automation supports the non-client area without any explicit help from the window. You can override and customize the support by using the [IRawElementProviderSimple](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-irawelementprovidersimple) interface that is retrieved by this function.

This function is particularly useful when you use it with the [ProviderOptions\_RefuseNonClientSupport](/en-us/windows/desktop/api/uiautomationcore/ne-uiautomationcore-provideroptions) flag, which disables the UI Automation default provider for the non-client area so that the window can supply its own provider.

The supported object IDs for controls in the non-client area include [OBJID\_WINDOW](/en-us/windows/desktop/WinAuto/object-identifiers)[, OBJID\_VSCROLL](/en-us/windows/desktop/WinAuto/object-identifiers), [OBJID\_HSCROLL](/en-us/windows/desktop/WinAuto/object-identifiers), [OBJID\_TITLEBAR](/en-us/windows/desktop/WinAuto/object-identifiers), [OBJID\_MENU](/en-us/windows/desktop/WinAuto/object-identifiers), and [OBJID\_SIZEGRIP](/en-us/windows/desktop/WinAuto/object-identifiers). For **OBJID\_TITLEBAR**, use the child ID to distinguish between the entire title bar and the buttons that it contains.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 8 [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2012 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcoreapi.h |
| **Library** | Uiautomationcore.lib |
| **DLL** | Uiautomationcore.dll |

## See also

[Functions for Providers](/en-us/windows/desktop/WinAuto/uiauto-functions)

---
