# UiaPropertyChangedEventArgs

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/ns-uiautomationcoreapi-uiapropertychangedeventargs)

# UiaPropertyChangedEventArgs structure (uiautomationcoreapi.h)

**Note**  This structure is deprecated.

Contains information about an event that is raised when a Microsoft UI Automation element property change occurs.

## Syntax

```
struct UiaPropertyChangedEventArgs {
  EventArgsType Type;
  int           EventId;
  PROPERTYID    PropertyId;
  VARIANT       OldValue;
  VARIANT       NewValue;
};
```

## Members

`Type`

Type: **[EventArgsType](/en-us/windows/desktop/api/uiautomationcoreapi/ne-uiautomationcoreapi-eventargstype)**

A value from the [EventArgsType](/en-us/windows/desktop/api/uiautomationcoreapi/ne-uiautomationcoreapi-eventargstype) enumerated type indicating the type of event.

`EventId`

Type: **int**

The identifier of the event. For a list of event identifiers, see [Event Identifiers](/en-us/windows/desktop/WinAuto/uiauto-event-ids).

`PropertyId`

Type: **PROPERTYID**

The identifier of the property that has changed. For a list of property IDs, see [Property Identifiers](/en-us/windows/desktop/WinAuto/uiauto-entry-propids).

`OldValue`

Type: **[VARIANT](/en-us/windows/desktop/WinAuto/variant-structure)**

A [VARIANT](/en-us/windows/desktop/WinAuto/variant-structure) containing the old value of the property.

`NewValue`

Type: **[VARIANT](/en-us/windows/desktop/WinAuto/variant-structure)**

A [VARIANT](/en-us/windows/desktop/WinAuto/variant-structure) containing the new value of the property.

## Remarks

The old value might not be set if the UI Automation provider cannot do so efficiently.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps only] |
| **Minimum supported server** | Windows Server 2003 [desktop apps only] |
| **Header** | uiautomationcoreapi.h |

---
