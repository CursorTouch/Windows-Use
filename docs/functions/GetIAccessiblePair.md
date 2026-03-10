# GetIAccessiblePair

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nf-uiautomationcore-iaccessibleex-getiaccessiblepair)

# IAccessibleEx::GetIAccessiblePair method (uiautomationcore.h)

Retrieves the [IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible) interface and child ID for this item.

## Syntax

```
HRESULT GetIAccessiblePair(
  [out] IAccessible **ppAcc,
  [out] long        *pidChild
);
```

## Parameters

`[out] ppAcc`

Type: **[IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible)\*\***

Receives a pointer to the [IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible) interface for this object, or the parent object if this is a child element.

`[out] pidChild`

Type: **long\***

Receives the child ID, or CHILDID\_SELF if this is not a child element.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[IAccessibleEx](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-iaccessibleex)

---
