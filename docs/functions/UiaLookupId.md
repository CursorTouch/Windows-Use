# UiaLookupId

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/nf-uiautomationcoreapi-uialookupid)

# UiaLookupId function (uiautomationcoreapi.h)

**Note**  This function is deprecated. Client applications should use the Microsoft UI Automation Component Object Model (COM) interfaces instead.

Gets the integer identifier that can be used in methods that require a PROPERTYID, PATTERNID, CONTROLTYPEID, TEXTATTRIBUTEID, or EVENTID.

## Syntax

```
int UiaLookupId(
  [in] AutomationIdentifierType type,
  [in] const GUID               *pGuid
);
```

## Parameters

`[in] type`

Type: **[AutomationIdentifierType](/en-us/windows/desktop/api/uiautomationcoreapi/ne-uiautomationcoreapi-automationidentifiertype)**

A value from the [AutomationIdentifierType](/en-us/windows/desktop/api/uiautomationcoreapi/ne-uiautomationcoreapi-automationidentifiertype) enumerated type that specifies the type of identifier to look up.

`[in] pGuid`

Type: **GUID\***

The address of the unique identifier of the property, pattern, control type, text attribute, or event.

## Return value

Type: **int**

Returns an integer identifier.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps only] |
| **Minimum supported server** | Windows Server 2003 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationcoreapi.h |
| **Library** | Uiautomationcore.lib |
| **DLL** | Uiautomationcore.dll |

## See also

**Conceptual**

[GUIDs](/en-us/windows/desktop/WinAuto/uiauto-guids)

[Property Identifiers](/en-us/windows/desktop/WinAuto/uiauto-entry-propids)

---
