# GetObjectForChild

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nf-uiautomationcore-iaccessibleex-getobjectforchild)

# IAccessibleEx::GetObjectForChild method (uiautomationcore.h)

Retrieves an [IAccessibleEx](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-iaccessibleex) interface representing the specified child of this element.

## Syntax

```
HRESULT GetObjectForChild(
  [in]  long          idChild,
  [out] IAccessibleEx **pRetVal
);
```

## Parameters

`[in] idChild`

Type: **long**

The identifier of the child element.

`[out] pRetVal`

Type: **[IAccessibleEx](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-iaccessibleex)\*\***

Receives a pointer to the [IAccessibleEx](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-iaccessibleex) interface.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

*pRetVal* returns **NULL** if this implementation does not use child IDs, or cannot provide an [IAccessibleEx](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-iaccessibleex) interface for the specified child, or itself represents a child element.

*idChild* must represent an actual MSAA child element, not an object that has its own [IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible) interface.

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
