# ElementFromIAccessibleBuildCache

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomation-elementfromiaccessiblebuildcache)

# IUIAutomation::ElementFromIAccessibleBuildCache method (uiautomationclient.h)

Retrieves a UI Automation element for the specified accessible object from a Microsoft Active Accessibility server, prefetches the requested properties and control patterns, and stores the prefetched items in the cache.

## Syntax

```
HRESULT ElementFromIAccessibleBuildCache(
  [in]          IAccessible               *accessible,
  [in]          int                       childId,
  [in]          IUIAutomationCacheRequest *cacheRequest,
  [out, retval] IUIAutomationElement      **element
);
```

## Parameters

`[in] accessible`

Type: **[IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible)\***

A pointer to the [IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible) interface of the accessible object.

`[in] childId`

Type: **int**

The child ID of the accessible object.

`[in] cacheRequest`

Type: **[IUIAutomationCacheRequest](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationcacherequest)\*\***

The address of the cache request that specifies the properties and control patterns to store in the cache.

`[out, retval] element`

Type: **[IUIAutomationElement](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationelement)\*\***

Receives a pointer to the UI Automation element.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

This method enables Microsoft UI Automation clients to get [IUIAutomationElement](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationelement) interfaces for accessible objects implemented by a Microsoft Active Accessibility server.

This method may fail if the server implements UI Automation provider interfaces alongside Microsoft Active Accessibility support.

The method returns E\_INVALIDARG if the underlying implementation of the UI Automation element is not a native Microsoft Active Accessibility server; that is, if a client attempts to retrieve the [IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible) interface for an element originally supported by a proxy object from Oleacc.dll, or by the UIA-to-MSAA Bridge.

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
