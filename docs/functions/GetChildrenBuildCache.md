# GetChildrenBuildCache

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationtextrange3-getchildrenbuildcache)

# IUIAutomationTextRange3::GetChildrenBuildCache method (uiautomationclient.h)

Returns the children and supplied properties and patterns for elements in a text range in a single cross-process call. This is equivalent to calling [GetChildren](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationtextrange-getchildren), but adds the standard build cache pattern.

## Syntax

```
HRESULT GetChildrenBuildCache(
  [in]          IUIAutomationCacheRequest *cacheRequest,
  [out, retval] IUIAutomationElementArray **children
);
```

## Parameters

`[in] cacheRequest`

An [IUIAutomationCacheRequest](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationcacherequest) specifying the properties and control patterns to be cached.

`[out, retval] children`

Returns the children, and each childâs properties or patterns, of the text range that meet the criteria of the supplied *cacheRequest*.

## Return value

Returns **S\_OK** if successful, otherwise an **HRESULT** error code.

## Remarks

Following the design of [GetChildren](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationtextrange-getchildren):

* Children that overlap with the text range, but are not entirely enclosed by it will also be included.
* When no children exist, an empty collection is returned.

As a result of a successful call, UI Automation clients are able call "Cached" APIs of [IUIAutomationElement](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationelement) that are provided in the *cacheRequest*, for example, [IUIAutomationElement::GetCachedPropertyValue](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-getcachedpropertyvalue).

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 10, version 1703 [desktop apps only] |
| **Minimum supported server** | None supported |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[IUIAutomationTextRange3](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationtextrange3)

[UI Automation Support for Textual Content](/en-us/windows/desktop/WinAuto/uiauto-ui-automation-textpattern-overview)

---
