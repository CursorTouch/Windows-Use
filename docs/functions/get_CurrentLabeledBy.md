# get_CurrentLabeledBy

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-get_currentlabeledby)

# IUIAutomationElement::get\_CurrentLabeledBy method (uiautomationclient.h)

Retrieves the element that contains the text label for this element.

This property is read-only.

## Syntax

```
HRESULT get_CurrentLabeledBy(
  IUIAutomationElement **retVal
);
```

## Parameters

`retVal`

## Return value

None

## Remarks

This property could be used to retrieve, for example, the static text label for a combo box.

This property maps to the Accessible Rich Internet Applications (ARIA) **labeledby** property.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[Automation Element Property IDs](/en-us/windows/desktop/WinAuto/uiauto-automation-element-propids)

[CachedLabeledBy](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-get_cachedlabeledby)

[IUIAutomationElement](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationelement)

**Reference**

---
