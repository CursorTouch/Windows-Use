# NormalizeElementBuildCache

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationtreewalker-normalizeelementbuildcache)

# IUIAutomationTreeWalker::NormalizeElementBuildCache method (uiautomationclient.h)

Retrieves the ancestor element nearest to the specified Microsoft UI Automation element in the tree view, prefetches the requested properties and control patterns, and stores the prefetched items in the cache.

## Syntax

```
HRESULT NormalizeElementBuildCache(
  [in]          IUIAutomationElement      *element,
  [in]          IUIAutomationCacheRequest *cacheRequest,
  [out, retval] IUIAutomationElement      **normalized
);
```

## Parameters

`[in] element`

Type: **[IUIAutomationElement](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationelement)\***

A pointer to the element from which to start the normalization.

`[in] cacheRequest`

Type: **[IUIAutomationCacheRequest](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationcacherequest)\***

A pointer to a cache request that specifies the properties and control patterns to cache on the returned element.

`[out, retval] normalized`

Type: **[IUIAutomationElement](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationelement)\*\***

Receives a pointer to the ancestor element nearest to the specified element in the tree view.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

The element is normalized by navigating up the ancestor chain in the tree until an element that satisfies the view condition (specified by a previous call to [IUIAutomationTreeWalker::Condition](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationtreewalker-get_condition)) is reached. If the root element is reached, the root element is returned, even if it does not satisfy the view condition.

This method is useful for applications that obtain references to UI Automation elements by hit-testing. The application might want to work only with specific types of elements, and can use [IUIAutomationTreeWalker::NormalizeElement](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationtreewalker-normalizeelement) to make sure that no matter what element is initially retrieved (for example, when a scroll bar gets the input focus), only the element of interest (such as a content element) is ultimately retrieved.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

---
