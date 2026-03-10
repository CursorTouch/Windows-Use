# get_HostRawElementProvider

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nf-uiautomationcore-irawelementprovidersimple-get_hostrawelementprovider)

# IRawElementProviderSimple::get\_HostRawElementProvider method (uiautomationcore.h)

Specifies the host provider for this element.

This property is read-only.

## Syntax

```
HRESULT get_HostRawElementProvider(
  IRawElementProviderSimple **pRetVal
);
```

## Parameters

`pRetVal`

## Return value

None

## Remarks

This property is generally the Microsoft UI Automation provider for the window of a custom control.
UI Automation uses this provider in combination with the custom provider. For example, the runtime identifier
of the element is usually obtained from the host provider.

A host provider must be returned in the following cases: when the element is a fragment root,
when the element is a simple element (such as a push button), and when the provider is a repositioning placeholder (for more information, see [Provider Repositioning](/en-us/windows/desktop/WinAuto/uiauto-serversideprovider)).
In other cases, the property should be **NULL**.

#### Examples

The following example returns the host provider for the window that hosts the control served by
this provider.

```
HRESULT STDMETHODCALLTYPE Provider::get_HostRawElementProvider(IRawElementProviderSimple** pRetVal)
{
    return UiaHostProviderFromHwnd(controlHWnd, pRetVal); 
}
```

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2003 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[IRawElementProviderSimple](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-irawelementprovidersimple)

[UiaHostProviderFromHwnd](/en-us/windows/desktop/api/uiautomationcoreapi/nf-uiautomationcoreapi-uiahostproviderfromhwnd)

---
