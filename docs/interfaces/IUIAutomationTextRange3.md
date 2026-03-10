# IUIAutomationTextRange3

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nn-uiautomationclient-iuiautomationtextrange3)

# IUIAutomationTextRange3 interface (uiautomationclient.h)

Extends the [IUIAutomationTextRange2](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationtextrange2) interface to support faster access to the underlying rich text data on a text range.

## Inheritance

The **IUIAutomationTextRange3** interface inherits from [IUIAutomationTextRange2](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationtextrange2). **IUIAutomationTextRange3** also has these types of members:

## Methods

The **IUIAutomationTextRange3** interface has these methods.

|  |
| --- |
| [IUIAutomationTextRange3::GetAttributeValues](nf-uiautomationclient-iuiautomationtextrange3-getattributevalues)   Returns all of the requested text attribute values for a text range in a single cross-process call. This is equivalent to calling GetAttributeValue, except it can retrieve multiple values instead of just one. |
| [IUIAutomationTextRange3::GetChildrenBuildCache](nf-uiautomationclient-iuiautomationtextrange3-getchildrenbuildcache)   Returns the children and supplied properties and patterns for elements in a text range in a single cross-process call. This is equivalent to calling GetChildren, but adds the standard build cache pattern. |
| [IUIAutomationTextRange3::GetEnclosingElementBuildCache](nf-uiautomationclient-iuiautomationtextrange3-getenclosingelementbuildcache)   Gets the enclosing element and supplied properties and patterns for an element in a text range in a single cross-process call. This is equivalent to calling GetEnclosingElement, but adds the standard build cache pattern. |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 10, version 1703 [desktop apps only] |
| **Minimum supported server** | None supported |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[IUIAutomationTextRange](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationtextrange)

[IUIAutomationTextRange2](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationtextrange2)

---
