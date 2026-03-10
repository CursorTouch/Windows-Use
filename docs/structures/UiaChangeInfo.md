# UiaChangeInfo

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/ns-uiautomationcore-uiachangeinfo)

# UiaChangeInfo structure (uiautomationcore.h)

Contains data about a UI Automation change that occurred.

## Syntax

```
struct UiaChangeInfo {
  int     uiaId;
  VARIANT payload;
  VARIANT extraInfo;
};
```

## Members

`uiaId`

Identifies the type of change info. Possible values are all the values of **Change Identifiers**, [Property Identifiers](/en-us/windows/desktop/WinAuto/uiauto-entry-propids), [Text Attribute Identifiers](/en-us/windows/desktop/WinAuto/uiauto-textattribute-ids), [Annotation Type Identifiers](/en-us/windows/desktop/WinAuto/uiauto-annotation-type-identifiers) and [Style Identifiers](/en-us/windows/desktop/WinAuto/uiauto-style-identifiers).

`payload`

Information about the type of change that occurred.

`extraInfo`

Detailed information about the change that occurred.

## Remarks

The provider can call [UiaRaiseChangesEvent](/en-us/windows/desktop/api/uiautomationcoreapi/nf-uiautomationcoreapi-uiaraisechangesevent) and pass in an array of **UiaChangeInfo** structs to notify clients of a related group of changes. The **payload** and **extraInfo** will vary depending on the **uiaId** populated in the **UiaChangeInfo** struct.

If there are multiple of any of these event types multiple **UiaChangeInfo** structs would be created. Below is a description of what these are for each pair of values.

| UiaId | payload | extraInfo |
| --- | --- | --- |
| **UIA\_SummaryChangeId** | VT\_BSTR A string describing the meaning of the change from an application point of view. | A constant ID value from the provider indicating the meaning of this event. |
| For UIA property changes, identified in the [Property Identifiers](/en-us/windows/desktop/WinAuto/uiauto-entry-propids) section. | Type is the type of the property and the value is the new value of the property. |  |
| For text attributes changes, identified in the [Text Attribute Identifiers](/en-us/windows/desktop/WinAuto/uiauto-textattribute-ids) section, **extraInfo** is not used. | Type is the type of the attribute and the value is the new value of the attribute. |  |
| For annotation changes, identified in the [Annotation Type Identifiers](/en-us/windows/desktop/WinAuto/uiauto-annotation-type-identifiers) section, **extraInfo** is not used. | VT\_BSTR For text, the characters from the range to which the annotation applies. |  |
| For style changes, identified in the [Style Identifiers](/en-us/windows/desktop/WinAuto/uiauto-style-identifiers) section, **extraInfo** is not used. | VT\_BSTR For text, the characters from the range to which the style applies. |  |

## Requirements

| Requirement | Value |
| --- | --- |
| **Header** | uiautomationcore.h |

---
