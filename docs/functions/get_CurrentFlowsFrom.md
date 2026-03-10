# get_CurrentFlowsFrom

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement2-get_currentflowsfrom)

# IUIAutomationElement2::get\_CurrentFlowsFrom method (uiautomationclient.h)

Retrieves an array of elements that indicates the reading order before the current element.

This property is read/write.

## Syntax

```
HRESULT get_CurrentFlowsFrom(
  IUIAutomationElementArray **retVal
);
```

## Parameters

`retVal`

## Return value

None

## Remarks

This property maps to the Microsoft Accessible Rich Internet Applications (ARIA) [x-ms-aria-flowfrom](/en-us/previous-versions/hh969192(v=vs.85)) property.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 8 [desktop apps only] |
| **Minimum supported server** | Windows Server 2012 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[CachedFlowsFrom](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement2-get_cachedflowsfrom)

[IUIAutomationElement2](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationelement2)

---
