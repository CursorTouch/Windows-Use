# UiaStructureChangedEventArgs

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/ns-uiautomationcoreapi-uiastructurechangedeventargs)

# UiaStructureChangedEventArgs structure (uiautomationcoreapi.h)

**Note**  This structure is deprecated.

Contains information about an event that is raised when the structure of the Microsoft UI Automation tree changes.

## Syntax

```
struct UiaStructureChangedEventArgs {
  EventArgsType       Type;
  int                 EventId;
  StructureChangeType StructureChangeType;
  int                 *pRuntimeId;
  int                 cRuntimeIdLen;
};
```

## Members

`Type`

Type: **[EventArgsType](/en-us/windows/desktop/api/uiautomationcoreapi/ne-uiautomationcoreapi-eventargstype)**

A value from the [EventArgsType](/en-us/windows/desktop/api/uiautomationcoreapi/ne-uiautomationcoreapi-eventargstype) enumerated type indicating the type of event.

`EventId`

Type: **int**

The identifier of the event. For a list of event identifiers, see [Event Identifiers](/en-us/windows/desktop/WinAuto/uiauto-event-ids).

`StructureChangeType`

Type: **[StructureChangeType](/en-us/windows/desktop/api/uiautomationcore/ne-uiautomationcore-structurechangetype)**

A value from the [StructureChangeType](/en-us/windows/desktop/api/uiautomationcore/ne-uiautomationcore-structurechangetype) enumerated type indicating the type of change that has taken place.

`pRuntimeId`

Type: **int\***

The address of an array of runtime identifiers for elements involved in the change.

`cRuntimeIdLen`

Type: **int**

The count of elements in the array.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps only] |
| **Minimum supported server** | Windows Server 2003 [desktop apps only] |
| **Header** | uiautomationcoreapi.h |

---
