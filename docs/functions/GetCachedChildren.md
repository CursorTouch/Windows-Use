# GetCachedChildren

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-getcachedchildren)

# IUIAutomationElement::GetCachedChildren method (uiautomationclient.h)

Retrieves the cached child elements of this UI Automation element.

## Syntax

```
HRESULT GetCachedChildren(
  [out, retval] IUIAutomationElementArray **children
);
```

## Parameters

`[out, retval] children`

Type: **[IUIAutomationElementArray](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationelementarray)\*\***

Receives a pointer to a collection of the cached child elements.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

The view of the returned collection is determined by the TreeFilter property of the [IUIAutomationCacheRequest](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationcacherequest) that was active when this element was obtained.

Children are cached only if the scope of the cache request included [TreeScope\_Subtree](/en-us/windows/desktop/api/uiautomationclient/ne-uiautomationclient-treescope), [TreeScope\_Children](/en-us/windows/desktop/api/uiautomationclient/ne-uiautomationclient-treescope), or [TreeScope\_Descendants](/en-us/windows/desktop/api/uiautomationclient/ne-uiautomationclient-treescope).

If the cache request specified that children were to be cached at this level, but there are no children, the value of this property is 0. However, if no request was made to cache children at this level, an attempt to retrieve the property returns an error.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

**Conceptual**

[GetCachedParent](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-getcachedparent)

[IUIAutomationElement](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationelement)

[Obtaining UI Automation Elements](/en-us/windows/desktop/WinAuto/uiauto-obtainingelements)

**Reference**

[UI Automation Tree Overview](/en-us/windows/desktop/WinAuto/uiauto-treeoverview)

---
