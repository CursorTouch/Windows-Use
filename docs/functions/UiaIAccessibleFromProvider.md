# UiaIAccessibleFromProvider

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/nf-uiautomationcoreapi-uiaiaccessiblefromprovider)

# UiaIAccessibleFromProvider function (uiautomationcoreapi.h)

Retrieves an [IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible) implementation that provides Microsoft Active Accessibility data on behalf of a Microsoft UI Automation provider.

## Syntax

```
HRESULT UiaIAccessibleFromProvider(
  [in]  IRawElementProviderSimple *pProvider,
  [in]  DWORD                     dwFlags,
  [out] IAccessible               **ppAccessible,
  [out] VARIANT                   *pvarChild
);
```

## Parameters

`[in] pProvider`

Type: **[IRawElementProviderSimple](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-irawelementprovidersimple)\***

A pointer to the UI Automation object.

`[in] dwFlags`

Type: **DWORD**

One of the following values:

#### UIA\_IAFP\_DEFAULT

#### UIA\_IAFP\_UNWRAP\_BRIDGE

`[out] ppAccessible`

Type: **[IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible)\*\***

Receives the pointer to the [IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible) implementation for the provider.

`[out] pvarChild`

Type: **[VARIANT](/en-us/windows/desktop/WinAuto/variant-structure)\***

Receives the child identifier of the accessible element in the **lVal** member.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this function succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

In most cases, this function retrieves a wrapper object, provided by Windows, that implements [IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible) on behalf of the [IRawElementProviderSimple](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-irawelementprovidersimple) object. If the provided **IRawElementProviderSimple** pointer is itself a wrapper object, this function retrieves the wrapped **IAccessible** pointer and returns that instead, to prevent the creation of multiple layers of wrappers.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 8 [desktop apps only] |
| **Minimum supported server** | Windows Server 2012 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationcoreapi.h |
| **Library** | Uiautomationcore.lib |
| **DLL** | Uiautomationcore.dll |

## See also

[Functions for Providers](/en-us/windows/desktop/WinAuto/uiauto-functions)

[UiaProviderFromIAccessible](/en-us/windows/desktop/api/uiautomationcoreapi/nf-uiautomationcoreapi-uiaproviderfromiaccessible)

---
