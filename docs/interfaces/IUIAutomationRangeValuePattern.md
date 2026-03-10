# IUIAutomationRangeValuePattern

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nn-uiautomationclient-iuiautomationrangevaluepattern)

# IUIAutomationRangeValuePattern interface (uiautomationclient.h)

Provides access to a control that presents a range of values.

## Inheritance

The **IUIAutomationRangeValuePattern** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **IUIAutomationRangeValuePattern** also has these types of members:

## Methods

The **IUIAutomationRangeValuePattern** interface has these methods.

|  |
| --- |
| [IUIAutomationRangeValuePattern::get\_CachedIsReadOnly](nf-uiautomationclient-iuiautomationrangevaluepattern-get_cachedisreadonly)   Retrieves a cached value that indicates whether the value of the element can be changed. |
| [IUIAutomationRangeValuePattern::get\_CachedLargeChange](nf-uiautomationclient-iuiautomationrangevaluepattern-get_cachedlargechange)   Retrieves, from the cache, the value that is added to or subtracted from the value of the control when a large change is made, such as when the PAGE DOWN key is pressed. |
| [IUIAutomationRangeValuePattern::get\_CachedMaximum](nf-uiautomationclient-iuiautomationrangevaluepattern-get_cachedmaximum)   Retrieves the cached maximum value of the control. |
| [IUIAutomationRangeValuePattern::get\_CachedMinimum](nf-uiautomationclient-iuiautomationrangevaluepattern-get_cachedminimum)   Retrieves the cached minimum value of the control. |
| [IUIAutomationRangeValuePattern::get\_CachedSmallChange](nf-uiautomationclient-iuiautomationrangevaluepattern-get_cachedsmallchange)   Retrieves, from the cache, the value that is added to or subtracted from the value of the control when a small change is made, such as when an arrow key is pressed. |
| [IUIAutomationRangeValuePattern::get\_CachedValue](nf-uiautomationclient-iuiautomationrangevaluepattern-get_cachedvalue)   Retrieves the cached value of the control. |
| [IUIAutomationRangeValuePattern::get\_CurrentIsReadOnly](nf-uiautomationclient-iuiautomationrangevaluepattern-get_currentisreadonly)   Indicates whether the value of the element can be changed. |
| [IUIAutomationRangeValuePattern::get\_CurrentLargeChange](nf-uiautomationclient-iuiautomationrangevaluepattern-get_currentlargechange)   Retrieves the value that is added to or subtracted from the value of the control when a large change is made, such as when the PAGE DOWN key is pressed. |
| [IUIAutomationRangeValuePattern::get\_CurrentMaximum](nf-uiautomationclient-iuiautomationrangevaluepattern-get_currentmaximum)   Retrieves the maximum value of the control. |
| [IUIAutomationRangeValuePattern::get\_CurrentMinimum](nf-uiautomationclient-iuiautomationrangevaluepattern-get_currentminimum)   Retrieves the minimum value of the control. |
| [IUIAutomationRangeValuePattern::get\_CurrentSmallChange](nf-uiautomationclient-iuiautomationrangevaluepattern-get_currentsmallchange)   Retrieves the value that is added to or subtracted from the value of the control when a small change is made, such as when an arrow key is pressed. |
| [IUIAutomationRangeValuePattern::get\_CurrentValue](nf-uiautomationclient-iuiautomationrangevaluepattern-get_currentvalue)   Retrieves the value of the control. |
| [IUIAutomationRangeValuePattern::SetValue](nf-uiautomationclient-iuiautomationrangevaluepattern-setvalue)   Sets the value of the control. (IUIAutomationRangeValuePattern.SetValue) |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[Control Pattern Interfaces for Clients](/en-us/windows/desktop/WinAuto/uiauto-client-controlpatterninterfaces)

---
