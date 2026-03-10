# GetObjectIdForProvider

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nf-uiautomationcore-iaccessiblehostingelementproviders-getobjectidforprovider)

# IAccessibleHostingElementProviders::GetObjectIdForProvider method (uiautomationcore.h)

Retrieves the object ID associated with a contained windowless Microsoft ActiveX control that implements Microsoft UI Automation.

## Syntax

```
HRESULT GetObjectIdForProvider(
  [in, optional] IRawElementProviderSimple *pProvider,
  [out]          long                      *pidObject
);
```

## Parameters

`[in, optional] pProvider`

Type: **[IRawElementProviderSimple](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-irawelementprovidersimple)\***

The provider for the windowless ActiveX control.

`[out] pidObject`

Type: **long\***

The object ID of the contained windowless ActiveX control.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 8 [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2012 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[IAccessibleHostingElementProviders](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-iaccessiblehostingelementproviders)

---
