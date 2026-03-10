# EventArgsType

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/ne-uiautomationcoreapi-eventargstype)

# EventArgsType enumeration (uiautomationcoreapi.h)

Contains values that specify the event type described by a [UiaEventArgs](/en-us/windows/desktop/api/uiautomationcoreapi/ns-uiautomationcoreapi-uiaeventargs) structure.

## Syntax

```
typedef enum EventArgsType {
  EventArgsType_Simple,
  EventArgsType_PropertyChanged,
  EventArgsType_StructureChanged,
  EventArgsType_AsyncContentLoaded,
  EventArgsType_WindowClosed,
  EventArgsType_TextEditTextChanged,
  EventArgsType_Changes,
  EventArgsType_Notification,
  EventArgsType_ActiveTextPositionChanged,
  EventArgsType_StructuredMarkup
} ;
```

## Constants

|  |
| --- |
| `EventArgsType_Simple` A simple event that does not provide data in the event arguments. |
| `EventArgsType_PropertyChanged` An event raised by calling the [UiaRaiseAutomationPropertyChangedEvent function](nf-uiautomationcoreapi-uiaraiseautomationpropertychangedevent). |
| `EventArgsType_StructureChanged` An event raised by calling the [UiaRaiseStructureChangedEvent function](nf-uiautomationcoreapi-uiaraisestructurechangedevent). |
| `EventArgsType_AsyncContentLoaded` An event raised by calling the [UiaRaiseAsyncContentLoadedEvent function](nf-uiautomationcoreapi-uiaraiseasynccontentloadedevent). |
| `EventArgsType_WindowClosed` An event raised when a window is closed. |
| `EventArgsType_TextEditTextChanged` An event raised by calling the [UiaRaiseTextEditTextChangedEvent function](nf-uiautomationcoreapi-uiaraisetextedittextchangedevent) |
| `EventArgsType_Changes` An event raised by calling the [UiaRaiseChangesEvent function](nf-uiautomationcoreapi-uiaraisechangesevent). |
| `EventArgsType_Notification` An event raised by calling the [UiaRaiseNotificationEvent function](nf-uiautomationcoreapi-uiaraisenotificationevent). |
| `EventArgsType_ActiveTextPositionChanged` An event raised by calling the [UiaRaiseActiveTextPositionChangedEvent function](nf-uiautomationcoreapi-uiaraiseactivetextpositionchangedevent). |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps only] |
| **Minimum supported server** | Windows Server 2003 [desktop apps only] |
| **Header** | uiautomationcoreapi.h (include UIAutomation.h) |

---
