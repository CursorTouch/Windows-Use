# UiaReturnRawElementProvider

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/nf-uiautomationcoreapi-uiareturnrawelementprovider)

# UiaReturnRawElementProvider function (uiautomationcoreapi.h)

Gets an interface to the UI Automation provider for a window.

## Syntax

```
LRESULT UiaReturnRawElementProvider(
  [in] HWND                      hwnd,
  [in] WPARAM                    wParam,
  [in] LPARAM                    lParam,
  [in] IRawElementProviderSimple *el
);
```

## Parameters

`[in] hwnd`

Type: **[HWND](/en-us/windows/desktop/WinProg/windows-data-types)**

The handle of the window containing the element served by the provider.

`[in] wParam`

Type: **[WPARAM](/en-us/windows/desktop/WinProg/windows-data-types)**

The *wParam* argument of the [WM\_GETOBJECT](/en-us/windows/win32/winauto/wm-getobject) message.

`[in] lParam`

Type: **[LPARAM](/en-us/windows/desktop/WinProg/windows-data-types)**

The *lParam* argument of the [WM\_GETOBJECT](/en-us/windows/win32/winauto/wm-getobject) message.

`[in] el`

Type: **[IRawElementProviderSimple](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-irawelementprovidersimple)\***

The UI Automation provider.

## Return value

Type: **[LRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

The key for the client process to connect to the server process through UI Automation.

This function returns zero when it is used to notify UI Automation that it is safe to remove the provider raised-event map. For more information, see Remarks.

## Remarks

This function is called by a control when it receives the [WM\_GETOBJECT](/en-us/windows/win32/winauto/wm-getobject) message, to provide UI Automation with the UI Automation provider for the control. The control should pass the *wParam* and *lParam* parameters to the **UiaReturnRawElementProvider** function without filtering them first, because filtering can cause problems with Microsoft Active Accessibility clients. The control's window procedure should return the result of calling **UiaReturnRawElementProvider**.

When Microsoft Active Accessibility clients are listening to events raised by a UI Automation provider, UI Automation maintains a map of the providers that have raised events. When the Microsoft Active Accessibility clients request further information, UI Automation uses the map to route the requests to the appropriate providers. When a window that previously returned providers has been destroyed, you should notify UI Automation by calling the **UiaReturnRawElementProvider** function as follows: `UiaReturnRawElementProvider(hwnd, 0, 0, NULL)`. This call tells UI Automation that it can safely remove all map entries that refer to the specified window. This call can save memory because it releases references to the providers being held by the raised-event map. The function returns zero when called with these special parameters. Microsoft recommends making this call from the [WM\_DESTROY](/en-us/windows/desktop/winmsg/wm-destroy) message handler of the window that returns the UI Automation providers.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2003 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcoreapi.h |
| **Library** | Uiautomationcore.lib |
| **DLL** | Uiautomationcore.dll |

---
