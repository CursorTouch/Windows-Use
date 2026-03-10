# get_CurrentCurrentSelectedItem

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationselectionpattern2-get_currentcurrentselecteditem)

# IUIAutomationSelectionPattern2::get\_CurrentCurrentSelectedItem method (uiautomationclient.h)

Gets an [IUIAutomationElement](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationelement) object representing the currently selected item.

This property is read-only.

## Syntax

```
HRESULT get_CurrentCurrentSelectedItem(
  IUIAutomationElement **retVal
);
```

## Parameters

`retVal`

## Return value

None

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 10, version 1709 [desktop apps only] |
| **Minimum supported server** | Windows Server 2016 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[IUIAutomationSelectionPattern2](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationselectionpattern2)

---
