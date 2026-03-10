# IUIAutomationOrCondition

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nn-uiautomationclient-iuiautomationorcondition)

# IUIAutomationOrCondition interface (uiautomationclient.h)

Represents a condition made up of multiple conditions, at least one of which must be true.

## Inheritance

The **IUIAutomationOrCondition** interface inherits from [IUIAutomationCondition](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationcondition). **IUIAutomationOrCondition** also has these types of members:

## Methods

The **IUIAutomationOrCondition** interface has these methods.

|  |
| --- |
| [IUIAutomationOrCondition::get\_ChildCount](nf-uiautomationclient-iuiautomationorcondition-get_childcount)   Retrieves the number of conditions that make up this "or" condition. |
| [IUIAutomationOrCondition::GetChildren](nf-uiautomationclient-iuiautomationorcondition-getchildren)   Retrieves the conditions that make up this "or" condition. |
| [IUIAutomationOrCondition::GetChildrenAsNativeArray](nf-uiautomationclient-iuiautomationorcondition-getchildrenasnativearray)   Retrieves the conditions that make up this "or" condition, as an ordinary array. |

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
