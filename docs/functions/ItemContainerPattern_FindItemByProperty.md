# ItemContainerPattern_FindItemByProperty

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/nf-uiautomationcoreapi-itemcontainerpattern_finditembyproperty)

# ItemContainerPattern\_FindItemByProperty function (uiautomationcoreapi.h)

**Note**  This function is deprecated. Client applications should use the Microsoft UI Automation Component Object Model (COM) interfaces instead.

Retrieves a node within a containing node, based on a specified property value.

## Syntax

```
HRESULT ItemContainerPattern_FindItemByProperty(
  [in]  HUIAPATTERNOBJECT hobj,
  [in]  HUIANODE          hnodeStartAfter,
  [in]  PROPERTYID        propertyId,
  [in]  VARIANT           value,
  [out] HUIANODE          *pFound
);
```

## Parameters

`[in] hobj`

Type: **HUIAPATTERNOBJECT**

The *control pattern* object.

`[in] hnodeStartAfter`

Type: **HUIANODE**

The node after which to start the search.

`[in] propertyId`

Type: **PROPERTYID**

The property identifier. For a list of property IDs, see [Property Identifiers](/en-us/windows/desktop/WinAuto/uiauto-entry-propids).

`[in] value`

Type: **[VARIANT](/en-us/windows/desktop/WinAuto/variant-structure)**

The value of the *propertyId* property.

`[out] pFound`

Type: **HUIANODE\***

The node of the matching element.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

Returns S\_OK if successful or an error value otherwise.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationcoreapi.h |
| **Library** | Uiautomationcore.lib |
| **DLL** | Uiautomationcore.dll |

---
