# AutomationIdentifierType

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/ne-uiautomationcoreapi-automationidentifiertype)

# AutomationIdentifierType enumeration (uiautomationcoreapi.h)

Contains values used in the [UiaLookupId](/en-us/windows/desktop/api/uiautomationcoreapi/nf-uiautomationcoreapi-uialookupid) function.

## Syntax

```
typedef enum AutomationIdentifierType {
  AutomationIdentifierType_Property,
  AutomationIdentifierType_Pattern,
  AutomationIdentifierType_Event,
  AutomationIdentifierType_ControlType,
  AutomationIdentifierType_TextAttribute,
  AutomationIdentifierType_LandmarkType,
  AutomationIdentifierType_Annotation,
  AutomationIdentifierType_Changes,
  AutomationIdentifierType_Style
} ;
```

## Constants

|  |
| --- |
| `AutomationIdentifierType_Property` Specifies a property ID. |
| `AutomationIdentifierType_Pattern` Specifies a control pattern ID. |
| `AutomationIdentifierType_Event` Specifies an event ID. |
| `AutomationIdentifierType_ControlType` Specifies a control type ID. |
| `AutomationIdentifierType_TextAttribute` Specifies a text attribute ID. |
| `AutomationIdentifierType_LandmarkType` Specifies a landmark type ID. |
| `AutomationIdentifierType_Annotation` Specifies an annotation ID. |
| `AutomationIdentifierType_Changes` Specifies a changes ID. |
| `AutomationIdentifierType_Style` Specifies a style ID. |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps only] |
| **Minimum supported server** | Windows Server 2003 [desktop apps only] |
| **Header** | uiautomationcoreapi.h (include UIAutomation.h) |

---
