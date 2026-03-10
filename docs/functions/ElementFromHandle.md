# ElementFromHandle

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomation-elementfromhandle)

# IUIAutomation::ElementFromHandle method (uiautomationclient.h)

Retrieves a UI Automation element for the specified window.

## Syntax

```
HRESULT ElementFromHandle(
  [in]          UIA_HWND             hwnd,
  [out, retval] IUIAutomationElement **element
);
```

## Parameters

`[in] hwnd`

Type: **UIA\_HWND**

The window handle.

`[out, retval] element`

Type: **[IUIAutomationElement](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationelement)\*\***

Receives a pointer to the element.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[IUIAutomation](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomation)

[IUIAutomation::ElementFromHandleBuildCache](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomation-elementfromhandlebuildcache)

---
