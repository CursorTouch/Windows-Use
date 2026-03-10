# UiaEventArgs

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/ns-uiautomationcoreapi-uiaeventargs)

# UiaEventArgs structure (uiautomationcoreapi.h)

**Note**  This structure is deprecated.

Contains information about a Microsoft UI Automation event.

## Syntax

```
struct UiaEventArgs {
  EventArgsType Type;
  int           EventId;
};
```

## Members

`Type`

Type: **[EventArgsType](/en-us/windows/desktop/api/uiautomationcoreapi/ne-uiautomationcoreapi-eventargstype)**

A value from the [EventArgsType](/en-us/windows/desktop/api/uiautomationcoreapi/ne-uiautomationcoreapi-eventargstype) enumerated type indicating the type of the event.

`EventId`

Type: **int**

The identifier of the event. For a list of event identifiers, see [Event Identifiers](/en-us/windows/desktop/WinAuto/uiauto-event-ids).

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps only] |
| **Minimum supported server** | Windows Server 2003 [desktop apps only] |
| **Header** | uiautomationcoreapi.h |

---
