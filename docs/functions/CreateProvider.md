# CreateProvider

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationproxyfactory-createprovider)

# IUIAutomationProxyFactory::CreateProvider method (uiautomationclient.h)

Creates a proxy object that provides Microsoft UI Automation support for a UI element.

## Syntax

```
HRESULT CreateProvider(
  [in]          UIA_HWND                  hwnd,
  [in]          LONG                      idObject,
  [in]          LONG                      idChild,
  [out, retval] IRawElementProviderSimple **provider
);
```

## Parameters

`[in] hwnd`

Type: **UIA\_HWND**

The window handle of the UI element.

`[in] idObject`

Type: **[LONG](/en-us/windows/desktop/WinProg/windows-data-types)**

The object ID. See Remarks.

`[in] idChild`

Type: **[LONG](/en-us/windows/desktop/WinProg/windows-data-types)**

The child ID. See Remarks.

`[out, retval] provider`

Type: **[IRawElementProviderSimple](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-irawelementprovidersimple)\*\***

Receives a pointer to the proxy object.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

The *idObject* parameter is normally [OBJID\_CLIENT](/en-us/windows/desktop/WinAuto/object-identifiers), and *idChild* is normally CHILDID\_SELF. However, when the method is called in response to a registered WinEvent, these values are from the event, specifying the subelement that raised the event.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

---
