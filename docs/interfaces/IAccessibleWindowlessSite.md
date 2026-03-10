# IAccessibleWindowlessSite

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/oleacc/nn-oleacc-iaccessiblewindowlesssite)

# IAccessibleWindowlessSite interface (oleacc.h)

A Microsoft ActiveX control site implements this interface to enable a windowless ActiveX control that has a Microsoft Active Accessibility implementation to express its accessibility. This interface enables the control container to reserve a range of object IDs that a windowless control can use to raise events, and enables the control container to provide an [IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible) pointer for the parent of the windowless control.

## Inheritance

The **IAccessibleWindowlessSite** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **IAccessibleWindowlessSite** also has these types of members:

## Methods

The **IAccessibleWindowlessSite** interface has these methods.

|  |
| --- |
| [IAccessibleWindowlessSite::AcquireObjectIdRange](nf-oleacc-iaccessiblewindowlesssite-acquireobjectidrange)   Acquires a range of object IDs from the control host and marks them as reserved by a specific windowless control. |
| [IAccessibleWindowlessSite::GetParentAccessible](nf-oleacc-iaccessiblewindowlesssite-getparentaccessible)   Retrieves an IAccessible pointer for the parent of a windowless Microsoft ActiveX control in the accessibility tree. |
| [IAccessibleWindowlessSite::QueryObjectIdRanges](nf-oleacc-iaccessiblewindowlesssite-queryobjectidranges)   Retrieves the object ID ranges that a particular windowless Microsoft ActiveX control has reserved. |
| [IAccessibleWindowlessSite::ReleaseObjectIdRange](nf-oleacc-iaccessiblewindowlesssite-releaseobjectidrange)   Releases an object ID range that was acquired by a previous call to the IAccessibleWindowlessSite::AcquireObjectIdRange method. |

## Remarks

The functions that manage object ID ranges expect the site object to maintain a list of ranges that have already been reserved. When the window that contains the ActiveX control receives a [WM\_GETOBJECT](/en-us/windows/win32/winauto/wm-getobject) message with an **LPARAM** value (object ID) that is in a reserved range, the window should call the [IAccessibleHandler::AccessibleObjectFromID](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccessiblehandler-accessibleobjectfromid) method to get an [IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible) object for that object ID.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 8 [desktop apps only] |
| **Minimum supported server** | Windows Server 2012 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | oleacc.h |

## See also

[IRawElementProviderWindowlessSite](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-irawelementproviderwindowlesssite)

---
