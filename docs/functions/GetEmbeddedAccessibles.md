# GetEmbeddedAccessibles

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nf-uiautomationcore-irawelementproviderhostingaccessibles-getembeddedaccessibles)

# IRawElementProviderHostingAccessibles::GetEmbeddedAccessibles method (uiautomationcore.h)

Retrieves the [IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible) interface pointers of the windowless Microsoft ActiveX controls that are hosted by this provider.

## Syntax

```
HRESULT GetEmbeddedAccessibles(
  [out, retval] SAFEARRAY **pRetVal
);
```

## Parameters

`[out, retval] pRetVal`

Type: **[SAFEARRAY](/en-us/windows/win32/api/oaidl/ns-oaidl-safearray)\*\***

Receives the [IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible) pointers of the hosted windowless ActiveX controls.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

An ActiveX control container with an existing [IRawElementProviderFragmentRoot](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-irawelementproviderfragmentroot) interface implements this method on the same object that implements **IRawElementProviderFragmentRoot**. When called, this method should query each contained windowless control for an [IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible) pointer and then add the pointer to the safe array.

This method should ignore providers that do not implement [IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible).

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 8 [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2012 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[IRawElementProviderHostingAccessibles](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-irawelementproviderhostingaccessibles)

---
