# NotificationKind

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/ne-uiautomationcore-notificationkind)

# NotificationKind enumeration (uiautomationcore.h)

Defines values that indicate the type of a notification event, and a hint to the listener about the processing of the event. For example, if multiple notifications are received, they should all be read, or only the last one should be read, and so on.

## Syntax

```
typedef enum NotificationKind {
  NotificationKind_ItemAdded = 0,
  NotificationKind_ItemRemoved = 1,
  NotificationKind_ActionCompleted = 2,
  NotificationKind_ActionAborted = 3,
  NotificationKind_Other = 4
} ;
```

## Constants

|  |
| --- |
| `NotificationKind_ItemAdded` Value: *0* The current element and/or the container has had something added to it that should be presented to the user. |
| `NotificationKind_ItemRemoved` Value: *1* The current element has had something removed from inside of it that should be presented to the user. |
| `NotificationKind_ActionCompleted` Value: *2* The current element has a notification that an action was completed. |
| `NotificationKind_ActionAborted` Value: *3* The current element has a notification that an action was aborted. |
| `NotificationKind_Other` Value: *4* The current element has a notification not an add, remove, completed, or aborted action. |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 10, version 1709 [desktop apps only] |
| **Minimum supported server** | Windows Server 2016 [desktop apps only] |
| **Header** | uiautomationcore.h (include UIAutomation.h, Uiautomationcore.h) |

---
