# get_CurrentIsContentElement

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-get_currentiscontentelement)

# IUIAutomationElement::get\_CurrentIsContentElement method (uiautomationclient.h)

Indicates whether the element is a content element.

This property is read-only.

## Syntax

```
HRESULT get_CurrentIsContentElement(
  BOOL *retVal
);
```

## Parameters

`retVal`

## Return value

None

## Remarks

A content element contains data that is presented to the user. Examples of content elements are the items in a list box or a button in a dialog box. Non-content elements, also called peripheral elements, are typically used to manipulate the content in a composite control; for example, the button on a drop-down control.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[Automation Element Property IDs](/en-us/windows/desktop/WinAuto/uiauto-automation-element-propids)

[CachedIsContentElement](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-get_cachediscontentelement)

[CurrentIsControlElement](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-get_currentiscontrolelement)

[IUIAutomationElement](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationelement)

**Reference**

---
