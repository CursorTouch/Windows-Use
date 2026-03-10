# IRawElementProviderSimple

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nn-uiautomationcore-irawelementprovidersimple)

# IRawElementProviderSimple interface (uiautomationcore.h)

Defines methods and properties that expose simple UI elements.

## Inheritance

The **IRawElementProviderSimple** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **IRawElementProviderSimple** also has these types of members:

## Methods

The **IRawElementProviderSimple** interface has these methods.

|  |
| --- |
| [IRawElementProviderSimple::get\_HostRawElementProvider](nf-uiautomationcore-irawelementprovidersimple-get_hostrawelementprovider)   Specifies the host provider for this element. |
| [IRawElementProviderSimple::get\_ProviderOptions](nf-uiautomationcore-irawelementprovidersimple-get_provideroptions)   Specifies the type of Microsoft UI Automation provider; for example, whether it is a client-side (proxy) or server-side provider. |
| [IRawElementProviderSimple::GetPatternProvider](nf-uiautomationcore-irawelementprovidersimple-getpatternprovider)   Retrieves a pointer to an object that provides support for a control pattern on a Microsoft UI Automation element. |
| [IRawElementProviderSimple::GetPropertyValue](nf-uiautomationcore-irawelementprovidersimple-getpropertyvalue)   Retrieves the value of a property supported by the Microsoft UI Automation provider. |

## Remarks

This interface can be implemented on:

* UI Automation provider for simple UI elements, such as buttons.
* Providers that add or override properties or control patterns on a UI element that already has a provider.

Providers for complex elements must also implement [IRawElementProviderFragment](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-irawelementproviderfragment) and, if they
are root elements, [IRawElementProviderFragmentRoot](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-irawelementproviderfragmentroot).

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2003 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[IRawElementProviderFragment](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-irawelementproviderfragment)

[IRawElementProviderFragmentRoot](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-irawelementproviderfragmentroot)

**Reference**

---
