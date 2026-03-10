# IRawElementProviderHostingAccessibles

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nn-uiautomationcore-irawelementproviderhostingaccessibles)

# IRawElementProviderHostingAccessibles interface (uiautomationcore.h)

This interface is implemented by a Microsoft UI Automation provider when the provider is the root of an accessibility tree that includes windowless controls that support Microsoft Active Accessibility. Because UI Automation and Microsoft Active Accessibility use different interfaces, this interface enables a client to discover the list of hosted Microsoft Active Accessibility controls in case it needs to treat them differently.

## Inheritance

The **IRawElementProviderHostingAccessibles** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **IRawElementProviderHostingAccessibles** also has these types of members:

## Methods

The **IRawElementProviderHostingAccessibles** interface has these methods.

|  |
| --- |
| [IRawElementProviderHostingAccessibles::GetEmbeddedAccessibles](nf-uiautomationcore-irawelementproviderhostingaccessibles-getembeddedaccessibles)   Retrieves the IAccessible interface pointers of the windowless Microsoft ActiveX controls that are hosted by this provider. |

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
