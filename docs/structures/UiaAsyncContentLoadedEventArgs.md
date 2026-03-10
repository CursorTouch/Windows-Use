# UiaAsyncContentLoadedEventArgs

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/ns-uiautomationcoreapi-uiaasynccontentloadedeventargs)

# UiaAsyncContentLoadedEventArgs structure (uiautomationcoreapi.h)

**Note**  This structure is deprecated.

Contains information about an event raised when content is being asynchronously loaded by a UI element.

## Syntax

```
struct UiaAsyncContentLoadedEventArgs {
  EventArgsType           Type;
  int                     EventId;
  AsyncContentLoadedState AsyncContentLoadedState;
  double                  PercentComplete;
};
```

## Members

`Type`

Type: **[EventArgsType](/en-us/windows/desktop/api/uiautomationcoreapi/ne-uiautomationcoreapi-eventargstype)**

A value from the [EventArgsType](/en-us/windows/desktop/api/uiautomationcoreapi/ne-uiautomationcoreapi-eventargstype) enumerated type indicating the type of the event.

`EventId`

Type: **int**

The identifier of the event. For a list of event identifiers, see [Event Identifiers](/en-us/windows/desktop/WinAuto/uiauto-event-ids).

`AsyncContentLoadedState`

Type: **[AsyncContentLoadedState](/en-us/windows/desktop/api/uiautomationcoreapi/ne-uiautomationcoreapi-asynccontentloadedstate)**

A value from the [AsyncContentLoadedState](/en-us/windows/desktop/api/uiautomationcoreapi/ne-uiautomationcoreapi-asynccontentloadedstate) enumerated type indicating the state of asynchronous loading.

`PercentComplete`

Type: **double**

The percentage of loading that has been completed.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps only] |
| **Minimum supported server** | Windows Server 2003 [desktop apps only] |
| **Header** | uiautomationcoreapi.h |

---
