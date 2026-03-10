# get_CurrentItemStatus

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-get_currentitemstatus)

# IUIAutomationElement::get\_CurrentItemStatus method (uiautomationclient.h)

Retrieves the description of the status of an item in an element.

This property is read-only.

## Syntax

```
HRESULT get_CurrentItemStatus(
  BSTR *retVal
);
```

## Parameters

`retVal`

## Return value

None

## Remarks

This property enables a client to ascertain whether an element is conveying status about an item. For example, an item associated with a contact in a messaging application might be "Busy" or "Connected".

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[Automation Element Property IDs](/en-us/windows/desktop/WinAuto/uiauto-automation-element-propids)

[CachedItemStatus](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-get_cacheditemstatus)

[IUIAutomationElement](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationelement)

**Reference**

---
