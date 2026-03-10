# get_RawViewCondition

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomation-get_rawviewcondition)

# IUIAutomation::get\_RawViewCondition method (uiautomationclient.h)

Retrieves a predefined [IUIAutomationCondition](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationcondition) interface that selects all UI elements in an unfiltered view.

This property is read-only.

## Syntax

```
HRESULT get_RawViewCondition(
  IUIAutomationCondition **condition
);
```

## Parameters

`condition`

## Return value

None

## Remarks

Used by itself, the condition is functionally identical to the one retrieved by [IUIAutomation::CreateTrueCondition](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomation-createtruecondition).

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[ContentViewCondition](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomation-get_contentviewcondition)

[ControlViewCondition](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomation-get_controlviewcondition)

[IUIAutomation](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomation)

**Reference**

---
