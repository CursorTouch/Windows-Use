# UiaWindowClosedEventArgs

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/ns-uiautomationcoreapi-uiawindowclosedeventargs)

# UiaWindowClosedEventArgs structure (uiautomationcoreapi.h)

**Note**  This structure is deprecated.

Contains information about an event that is raised when one or more windows closes.

## Syntax

```
struct UiaWindowClosedEventArgs {
  EventArgsType Type;
  int           EventId;
  int           *pRuntimeId;
  int           cRuntimeIdLen;
};
```

## Members

`Type`

Type: **[EventArgsType](/en-us/windows/desktop/api/uiautomationcoreapi/ne-uiautomationcoreapi-eventargstype)**

A value from the [EventArgsType](/en-us/windows/desktop/api/uiautomationcoreapi/ne-uiautomationcoreapi-eventargstype) enumerated type indicating the type of event.

`EventId`

Type: **int**

The event identifier. For a list of event identifiers, see [Event Identifiers](/en-us/windows/desktop/WinAuto/uiauto-event-ids).

`pRuntimeId`

Type: **int\***

The address of an array of the UI Automation runtime identifiers of windows that have closed.

`cRuntimeIdLen`

Type: **int**

The count of elements in the array.

## Remarks

This event is raised for any window (HWND) that closes, not just top-level windows.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps only] |
| **Minimum supported server** | Windows Server 2003 [desktop apps only] |
| **Header** | uiautomationcoreapi.h |

---
