# IUIAutomationAndCondition

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nn-uiautomationclient-iuiautomationandcondition)

# IUIAutomationAndCondition interface (uiautomationclient.h)

Exposes properties and methods that Microsoft UI Automation client applications can use to retrieve information about an AND-based property condition.

## Inheritance

The **IUIAutomationAndCondition** interface inherits from [IUIAutomationCondition](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationcondition). **IUIAutomationAndCondition** also has these types of members:

## Methods

The **IUIAutomationAndCondition** interface has these methods.

|  |
| --- |
| [IUIAutomationAndCondition::get\_ChildCount](nf-uiautomationclient-iuiautomationandcondition-get_childcount)   Retrieves the number of conditions that make up this "and" condition. |
| [IUIAutomationAndCondition::GetChildren](nf-uiautomationclient-iuiautomationandcondition-getchildren)   Retrieves the conditions that make up this "and" condition. |
| [IUIAutomationAndCondition::GetChildrenAsNativeArray](nf-uiautomationclient-iuiautomationandcondition-getchildrenasnativearray)   Retrieves the conditions that make up this "and" condition, as an ordinary array. |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[IUIAutomationCondition](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationcondition)

[Property Condition Interfaces for Clients](/en-us/windows/desktop/WinAuto/uiauto-client-propconditioninterfaces)

---
