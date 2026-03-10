# get_CurrentAriaRole

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-get_currentariarole)

# IUIAutomationElement::get\_CurrentAriaRole method (uiautomationclient.h)

Retrieves the Accessible Rich Internet Applications (ARIA) role of the element.

This property is read-only.

## Syntax

```
HRESULT get_CurrentAriaRole(
  BSTR *retVal
);
```

## Parameters

`retVal`

## Return value

None

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[Automation Element Property IDs](/en-us/windows/desktop/WinAuto/uiauto-automation-element-propids)

[CachedAriaRole](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-get_cachedariarole)

**Conceptual**

[IUIAutomationElement](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationelement)

**Other Resources**

**Reference**

[UI Automation for W3C Accessible Rich Internet Applications Specification](/en-us/windows/desktop/WinAuto/uiauto-ariaspecification)

[WAI-ARIA Overview](https://www.w3.org/WAI/intro/aria)

---
