# get_AutoSetFocus

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomation2-get_autosetfocus)

# IUIAutomation2::get\_AutoSetFocus method (uiautomationclient.h)

Specifies whether calls to UI Automation control pattern methods automatically set focus to the target element.

This property is read/write.

## Syntax

```
HRESULT get_AutoSetFocus(
  BOOL *autoSetFocus
);
```

## Parameters

`autoSetFocus`

## Return value

None

## Remarks

By default, most UI Automation methods that perform an action on an element, such as [IUIAutomationInvokePattern::Invoke](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationinvokepattern-invoke) and [IUIAutomationValuePattern::SetValue](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationvaluepattern-setvalue), set focus to the element before performing the action. For most applications, setting the focus results in a more consistent user experience. In situations where setting the focus would be disruptive, such as automating a drop-down menu, you can set **AutoSetFocus** to FALSE to prevent UI Automation methods from setting the focus.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 8 [desktop apps only] |
| **Minimum supported server** | Windows Server 2012 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |
| **DLL** | UIAutomationCore.dll |

## See also

[IUIAutomation2](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomation2)

---
