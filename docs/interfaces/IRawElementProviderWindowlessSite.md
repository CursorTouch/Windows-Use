# IRawElementProviderWindowlessSite

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nn-uiautomationcore-irawelementproviderwindowlesssite)

# IRawElementProviderWindowlessSite interface (uiautomationcore.h)

A Microsoft ActiveX control site implements this interface to enable a Microsoft UI Automation-enabled ActiveX control to express its accessibility. This interface enables the control container to provide an [IRawElementProviderFragment](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-irawelementproviderfragment) pointer for the parent or siblings of the windowless ActiveX control, and to provide a runtime ID that is unique to the control site.

## Inheritance

The **IRawElementProviderWindowlessSite** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **IRawElementProviderWindowlessSite** also has these types of members:

## Methods

The **IRawElementProviderWindowlessSite** interface has these methods.

|  |
| --- |
| [IRawElementProviderWindowlessSite::GetAdjacentFragment](nf-uiautomationcore-irawelementproviderwindowlesssite-getadjacentfragment)   Retrieves a fragment pointer for a fragment that is adjacent to the windowless Microsoft ActiveX control owned by this control site. |
| [IRawElementProviderWindowlessSite::GetRuntimeIdPrefix](nf-uiautomationcore-irawelementproviderwindowlesssite-getruntimeidprefix)   Retrieves a Microsoft UI Automation runtime ID that is unique to the windowless Microsoft ActiveX control site. |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 8 [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2012 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[IAccessibleWindowlessSite](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessiblewindowlesssite)

---
