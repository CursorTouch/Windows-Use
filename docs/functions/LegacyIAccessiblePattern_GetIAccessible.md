# LegacyIAccessiblePattern_GetIAccessible

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/nf-uiautomationcoreapi-legacyiaccessiblepattern_getiaccessible)

# LegacyIAccessiblePattern\_GetIAccessible function (uiautomationcoreapi.h)

**Note**  This function is deprecated. Client applications should use the Microsoft UI Automation Component Object Model (COM) interfaces instead.

Retrieves an [IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible) object that corresponds to the UI Automation element.

## Syntax

```
HRESULT LegacyIAccessiblePattern_GetIAccessible(
  [in]  HUIAPATTERNOBJECT hobj,
  [out] IAccessible       **pAccessible
);
```

## Parameters

`[in] hobj`

Type: **HUIAPATTERNOBJECT**

A control pattern object.

`[out] pAccessible`

Type: **[IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible)\*\***

The address of a variable that receives a pointer to an [IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible) interface for the accessible object.

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
