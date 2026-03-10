# IValueProvider

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nn-uiautomationcore-ivalueprovider)

# IValueProvider interface (uiautomationcore.h)

Provides access
to controls that have an intrinsic value that does not span a range, and that can be represented as a string.

## Inheritance

The **IValueProvider** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **IValueProvider** also has these types of members:

## Methods

The **IValueProvider** interface has these methods.

|  |
| --- |
| [IValueProvider::get\_IsReadOnly](nf-uiautomationcore-ivalueprovider-get_isreadonly)   Indicates whether the value of a control is read-only. (IValueProvider.get\_IsReadOnly) |
| [IValueProvider::get\_Value](nf-uiautomationcore-ivalueprovider-get_value)   The value of the control. |
| [IValueProvider::SetValue](nf-uiautomationcore-ivalueprovider-setvalue)   Sets the value of control. |

## Remarks

The value of the control may or may not be editable depending on the control and its settings.

Implemented on a Microsoft UI Automation provider that must support the [Value](/en-us/windows/desktop/WinAuto/uiauto-implementingvalue) control pattern.

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
