# GetEnclosingElementBuildCache

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationtextrange3-getenclosingelementbuildcache)

# IUIAutomationTextRange3::GetEnclosingElementBuildCache method (uiautomationclient.h)

Gets the enclosing element and supplied properties and patterns for an element in a text range in a single cross-process call. This is equivalent to calling [GetEnclosingElement](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationtextrange-getenclosingelement), but adds the standard build cache pattern.

## Syntax

```
HRESULT GetEnclosingElementBuildCache(
  [in]          IUIAutomationCacheRequest *cacheRequest,
  [out, retval] IUIAutomationElement      **enclosingElement
);
```

## Parameters

`[in] cacheRequest`

An [IUIAutomationCacheRequest](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationcacherequest) specifying the properties and control patterns to be cached.

`[out, retval] enclosingElement`

Returns the enclosing element (and properties/patterns) of the text range if it meets the criteria of the supplied *cacheRequest*.

## Return value

Returns **S\_OK** if successful, otherwise an **HRESULT** error code.

## Remarks

Following the design of [GetEnclosingElement](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationtextrange-getenclosingelement):

* Gets the all-inclusive, innermost enclosing element of a text range and the supplied properties of the element.

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
