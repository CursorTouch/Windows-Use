# CreatePropertyConditionEx

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomation-createpropertyconditionex)

# IUIAutomation::CreatePropertyConditionEx method (uiautomationclient.h)

Creates a condition that selects elements that have a property with the specified value, using optional flags.

## Syntax

```
HRESULT CreatePropertyConditionEx(
  [in]          PROPERTYID             propertyId,
  [in]          VARIANT                value,
  [in]          PropertyConditionFlags flags,
  [out, retval] IUIAutomationCondition **newCondition
);
```

## Parameters

`[in] propertyId`

Type: **PROPERTYID**

The property identifier. For a list of property IDs, see [Property Identifiers](/en-us/windows/desktop/WinAuto/uiauto-entry-propids).

`[in] value`

Type: **[RECT](/en-us/windows/desktop/api/windef/ns-windef-rect)**

The property value.

`[in] flags`

Type: **[PropertyConditionFlags](/en-us/windows/desktop/api/uiautomationclient/ne-uiautomationclient-propertyconditionflags)**

The attributes of the condition. Use [PropertyConditionFlags\_IgnoreCase](/en-us/windows/desktop/api/uiautomationclient/ne-uiautomationclient-propertyconditionflags) to create a property condition that is not case-sensitive

`[out, retval] newCondition`

Type: **[IUIAutomationCondition](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationcondition)\*\***

Receives a pointer to the new condition.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[Best Practices for Using Safe Arrays](/en-us/windows/desktop/WinAuto/uiauto-workingwithsafearrays)

**Conceptual**

[CreatePropertyCondition](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomation-createpropertycondition)

[FindAll](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-findall)

[FindAllBuildCache](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-findallbuildcache)

[FindFirst](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-findfirst)

[FindFirstBuildCache](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-findfirstbuildcache)

[IUIAutomation](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomation)

[IUIAutomationCondition](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationcondition)

**Reference**

---
