# IRangeValueProvider

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nn-uiautomationcore-irangevalueprovider)

# IRangeValueProvider interface (uiautomationcore.h)

Provides access to controls that can be set to a value within a range.

## Inheritance

The **IRangeValueProvider** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **IRangeValueProvider** also has these types of members:

## Methods

The **IRangeValueProvider** interface has these methods.

|  |
| --- |
| [IRangeValueProvider::get\_IsReadOnly](nf-uiautomationcore-irangevalueprovider-get_isreadonly)   Indicates whether the value of a control is read-only. (IRangeValueProvider.get\_IsReadOnly) |
| [IRangeValueProvider::get\_LargeChange](nf-uiautomationcore-irangevalueprovider-get_largechange)   Specifies the value that is added to or subtracted from the IRangeValueProvider::Value property when a large change is made, such as when the PAGE DOWN key is pressed. |
| [IRangeValueProvider::get\_Maximum](nf-uiautomationcore-irangevalueprovider-get_maximum)   Specifies the maximum range value supported by the control. |
| [IRangeValueProvider::get\_Minimum](nf-uiautomationcore-irangevalueprovider-get_minimum)   Specifies the minimum range value supported by the control. |
| [IRangeValueProvider::get\_SmallChange](nf-uiautomationcore-irangevalueprovider-get_smallchange)   Specifies the value that is added to or subtracted from the IRangeValueProvider::Value property when a small change is made, such as when an arrow key is pressed. |
| [IRangeValueProvider::get\_Value](nf-uiautomationcore-irangevalueprovider-get_value)   Specifies the value of the control. |
| [IRangeValueProvider::SetValue](nf-uiautomationcore-irangevalueprovider-setvalue)   Sets the value of the control. (IRangeValueProvider.SetValue) |

## Remarks

Implemented on a Microsoft UI Automation provider that must support the [RangeValue](/en-us/windows/desktop/WinAuto/uiauto-implementingrangevalue) control pattern.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2003 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[UI Automation Providers Overview](/en-us/windows/desktop/WinAuto/uiauto-providersoverview)

---
