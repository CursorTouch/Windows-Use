# IAccessibleHostingElementProviders

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nn-uiautomationcore-iaccessiblehostingelementproviders)

# IAccessibleHostingElementProviders interface (uiautomationcore.h)

A Microsoft Active Accessibility object implements this interface when the object is the root of an accessibility tree that includes windowless Microsoft ActiveX controls that implement Microsoft UI Automation. Because Microsoft Active Accessibility and UI Automation use different interfaces, this interface enables a client to discover the list of hosted windowless ActiveX controls that support UI Automation in case the client needs to treat them differently.

## Inheritance

The **IAccessibleHostingElementProviders** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **IAccessibleHostingElementProviders** also has these types of members:

## Methods

The **IAccessibleHostingElementProviders** interface has these methods.

|  |
| --- |
| [IAccessibleHostingElementProviders::GetEmbeddedFragmentRoots](nf-uiautomationcore-iaccessiblehostingelementproviders-getembeddedfragmentroots)   Retrieves the Microsoft Active Accessibility providers of all windowless Microsoft ActiveX controls that have a Microsoft UI Automation provider implementation, and are hosted in a Microsoft Active Accessibility object that implements the IAccessibleHostingElementProviders interface. |
| [IAccessibleHostingElementProviders::GetObjectIdForProvider](nf-uiautomationcore-iaccessiblehostingelementproviders-getobjectidforprovider)   Retrieves the object ID associated with a contained windowless Microsoft ActiveX control that implements Microsoft UI Automation. |

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
