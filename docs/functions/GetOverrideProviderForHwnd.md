# GetOverrideProviderForHwnd

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nf-uiautomationcore-irawelementproviderhwndoverride-getoverrideproviderforhwnd)

# IRawElementProviderHwndOverride::GetOverrideProviderForHwnd method (uiautomationcore.h)

Gets a UI Automation provider for the specified element.

## Syntax

```
HRESULT GetOverrideProviderForHwnd(
  [in]          HWND                      hwnd,
  [out, retval] IRawElementProviderSimple **pRetVal
);
```

## Parameters

`[in] hwnd`

Type: **[HWND](/en-us/windows/desktop/WinProg/windows-data-types)**

The window handle of the element.

`[out, retval] pRetVal`

Type: **[IRawElementProviderSimple](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-irawelementprovidersimple)\*\***

Receives a pointer to the new provider for the specified window, or **NULL** if the provider is not being overridden.
This parameter is passed uninitialized.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

This method is implemented by fragment roots that contain window-based child elements.
By default, controls hosted in windows are served by default providers in addition to any custom providers.
The default providers treat all windows within a parent window as siblings. If you want to restructure the UI Automation
tree so that one window-based control is seen as a child of another, you must override the default provider by implementing
this method on the fragment root. The returned provider can supply additional properties or override properties of the
specified component.

The returned provider must be part of the fragment tree. It can supply additional properties or
override properties of the specified component.

If the returned provider implements [IRawElementProviderFragment](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-irawelementproviderfragment),
the provider should be part of the fragment's tree and be reachable by navigating from the fragment's root.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2003 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[IRawElementProviderHwndOverride](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-irawelementproviderhwndoverride)

---
