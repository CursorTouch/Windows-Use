# get_CurrentSmallChange

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationrangevaluepattern-get_currentsmallchange)

# IUIAutomationRangeValuePattern::get\_CurrentSmallChange method (uiautomationclient.h)

Retrieves the value that is added to or subtracted from the value of the control when a small change is made, such as when an arrow key is pressed.

This property is read-only.

## Syntax

```
HRESULT get_CurrentSmallChange(
  double *retVal
);
```

## Parameters

`retVal`

## Return value

None

## Remarks

The SmallChange property can support a Not a Number (NaN) value. When retrieving this property, a client can use the [\_isnan](/en-us/previous-versions/visualstudio/visual-studio-6.0/aa298428(v=vs.60)) function to determine whether the property is a NaN value.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[IUIAutomationRangeValuePattern](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationrangevaluepattern)

[IUIAutomationRangeValuePattern::CurrentLargeChange](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationrangevaluepattern-get_currentlargechange)

---
