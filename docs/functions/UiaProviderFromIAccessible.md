# UiaProviderFromIAccessible

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/nf-uiautomationcoreapi-uiaproviderfromiaccessible)

# UiaProviderFromIAccessible function (uiautomationcoreapi.h)

Creates a Microsoft UI Automation provider based on the specified Microsoft Active Accessibility object.

## Syntax

```
HRESULT UiaProviderFromIAccessible(
  [in]  IAccessible               *pAccessible,
  [in]  long                      idChild,
  [in]  DWORD                     dwFlags,
  [out] IRawElementProviderSimple **ppProvider
);
```

## Parameters

`[in] pAccessible`

Type: **[IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible)\***

A pointer to the Microsoft Active Accessibility object.

`[in] idChild`

Type: **long**

The child ID of the Microsoft Active Accessibility object.

`[in] dwFlags`

Type: **DWORD**

One of the following values:

#### UIA\_PFIA\_DEFAULT

#### UIA\_PFIA\_UNWRAP\_BRIDGE

`[out] ppProvider`

Type: **[IRawElementProviderSimple](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-irawelementprovidersimple)\*\***

The new UI Automation provider.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this function succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

UI Automation provides backward compatibility for Microsoft Active Accessibility providers by supplying a proxy for them, called the Microsoft Active Accessibility to UI Automation proxy. This proxy is created automatically when a window responds to a [WM\_GETOBJECT](/en-us/windows/win32/winauto/wm-getobject) message by returning a Microsoft Active Accessibility provider. Use **UiaProviderFromIAccessible** when you need to create a Microsoft Active Accessibility to UI Automation proxy manually; for example, when implementing the [IAccessibleEx](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-iaccessibleex) interface.

Some properties, such as LabeledBy, must be expressed as a UI Automation provider. An [IAccessibleEx](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-iaccessibleex) provider can use **UiaProviderFromIAccessible** to wrap an [IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible) object to return it as the value of the LabeledBy property.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 8 [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2012 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcoreapi.h |
| **Library** | Uiautomationcore.lib |
| **DLL** | Uiautomationcore.dll |

## See also

[Functions for Providers](/en-us/windows/desktop/WinAuto/uiauto-functions)

[UiaIAccessibleFromProvider](/en-us/windows/desktop/api/uiautomationcoreapi/nf-uiautomationcoreapi-uiaiaccessiblefromprovider)

---
