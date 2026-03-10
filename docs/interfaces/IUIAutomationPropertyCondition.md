# IUIAutomationPropertyCondition

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nn-uiautomationclient-iuiautomationpropertycondition)

# IUIAutomationPropertyCondition interface (uiautomationclient.h)

Represents a condition based on a property value that is used to find UI Automation elements.

## Inheritance

The **IUIAutomationPropertyCondition** interface inherits from the IUIAutomationCondition interface.

## Methods

The **IUIAutomationPropertyCondition** interface has these methods.

|  |
| --- |
| [IUIAutomationPropertyCondition::get\_PropertyConditionFlags](nf-uiautomationclient-iuiautomationpropertycondition-get_propertyconditionflags)   Retrieves a set of flags that specify how the condition is applied. |
| [IUIAutomationPropertyCondition::get\_PropertyId](nf-uiautomationclient-iuiautomationpropertycondition-get_propertyid)   Retrieves the identifier of the property on which this condition is based. |
| [IUIAutomationPropertyCondition::get\_PropertyValue](nf-uiautomationclient-iuiautomationpropertycondition-get_propertyvalue)   Retrieves the property value that must be matched for the condition to be true. |

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
