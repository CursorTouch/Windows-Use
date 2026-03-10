# put_TreeScope

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationcacherequest-put_treescope)

# IUIAutomationCacheRequest::put\_TreeScope method (uiautomationclient.h)

Specifies the scope of caching.

This property is read/write.

## Syntax

```
HRESULT put_TreeScope(
  TreeScope scope
);
```

## Parameters

`scope`

## Return value

None

## Remarks

When an element is retrieved, caching can be performed for only the element itself (the default behavior), or for the element and its children or descendants. This property describes the scope of the request.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[Caching UI Automation Properties and Control Patterns](/en-us/windows/desktop/WinAuto/uiauto-cachingforclients)

**Conceptual**

[IUIAutomationCacheRequest](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationcacherequest)

[Obtaining UI Automation Elements](/en-us/windows/desktop/WinAuto/uiauto-obtainingelements)

**Reference**

---
