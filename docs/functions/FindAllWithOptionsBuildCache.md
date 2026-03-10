# FindAllWithOptionsBuildCache

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement7-findallwithoptionsbuildcache)

# IUIAutomationElement7::FindAllWithOptionsBuildCache method (uiautomationclient.h)

Finds all matching elements in the specified order, but also caches their properties and patterns.

## Syntax

```
HRESULT FindAllWithOptionsBuildCache(
  [in]          TreeScope                 scope,
  [in]          IUIAutomationCondition    *condition,
  [in]          IUIAutomationCacheRequest *cacheRequest,
  [in]          TreeTraversalOptions      traversalOptions,
  [in]          IUIAutomationElement      *root,
  [out, retval] IUIAutomationElementArray **found
);
```

## Parameters

`[in] scope`

Type: **[TreeScope](ne-uiautomationclient-treescope)**

The scope of the request.

When an element is retrieved, caching can be performed for only the element itself (the default behavior), or for the element and its children or descendants. This property describes the scope of the request.

`[in] condition`

Type: **[IUIAutomationCondition](nn-uiautomationclient-iuiautomationcondition)**

The primary interface for conditions used in filtering when searching for elements in the UI Automation tree.

`[in] cacheRequest`

Type: **[IUIAutomationCacheRequest](nn-uiautomationclient-iuiautomationcacherequest)**

A pointer to a cache request that specifies the control patterns and properties to include in the cache.

`[in] traversalOptions`

Type: **[TreeTraversalOptions](ne-uiautomationclient-treetraversaloptions)**

The tree navigation order.

`[in] root`

Type: **[IUIAutomationElement](nn-uiautomationclient-iuiautomationelement)**

A pointer to the element with which to begin the search.

`[out, retval] found`

Receives a pointer to an array of matching elements. Returns an empty array if no matching element is found.

## Return value

Returns **S\_OK** if successful, otherwise an **HRESULT** error code.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 10, version 1703 [desktop apps only] |
| **Minimum supported server** | Windows Server 2016 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |
| **DLL** | UIAutomationCore.dll |

## See also

[IUIAutomationElement7](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationelement7)

---
