# ConvertReturnedElement

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nf-uiautomationcore-iaccessibleex-convertreturnedelement)

# IAccessibleEx::ConvertReturnedElement method (uiautomationcore.h)

Retrieves the [IAccessibleEx](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-iaccessibleex) interface of an element returned as a property value.

## Syntax

```
HRESULT ConvertReturnedElement(
  [in]  IRawElementProviderSimple *pIn,
  [out] IAccessibleEx             **ppRetValOut
);
```

## Parameters

`[in] pIn`

Type: **[IRawElementProviderSimple](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-irawelementprovidersimple)\***

Pointer to the [IRawElementProviderSimple](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-irawelementprovidersimple) interface that was retrieved as a property.

`[out] ppRetValOut`

Type: **[IAccessibleEx](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-iaccessibleex)\*\***

Receives a pointer to the [IAccessibleEx](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-iaccessibleex) interface of the element.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

This method is implemented by the bridge between Microsoft UI Automation and Microsoft Active Accessibility. Most other implementations should return E\_NOTIMPL after setting *ppRetValOut* to **NULL**.

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
