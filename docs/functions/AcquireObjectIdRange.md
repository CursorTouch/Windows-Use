# AcquireObjectIdRange

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/oleacc/nf-oleacc-iaccessiblewindowlesssite-acquireobjectidrange)

# IAccessibleWindowlessSite::AcquireObjectIdRange method (oleacc.h)

Acquires a range of object IDs from the control host and marks them as reserved by a specific windowless control.

## Syntax

```
HRESULT AcquireObjectIdRange(
  [in]           long               rangeSize,
  [in, optional] IAccessibleHandler *pRangeOwner,
  [out]          long               *pRangeBase
);
```

## Parameters

`[in] rangeSize`

The size of the object ID range that is being requested.

`[in, optional] pRangeOwner`

The windowless control that is requesting the range.

`[out] pRangeBase`

The first object ID in the acquired range.

## Return value

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

To avoid using an object ID that belongs to another windowless control, a control should acquire an object ID range before calling the [NotifyWinEvent](/en-us/windows/desktop/api/winuser/nf-winuser-notifywinevent) function. A control should acquire enough object IDs for all of its contained accessible objects. For example, a tree control with 100 children would reserve at least 101 object IDs, one for the root, and one for each child. A tree control that is expected to grow would reserve as many object IDs as expected. If the tree control is expected to grow by several hundred children, it would reserve a range of 1000 IDs just to be safe.

When the window that contains the Microsoft ActiveX control receives a [WM\_GETOBJECT](/en-us/windows/win32/winauto/wm-getobject) message with an **LPARAM** value (object ID) that is in a reserved range, it should call the [IAccessibleHandler::AccessibleObjectFromID](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccessiblehandler-accessibleobjectfromid) method to get an [IAccessible](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessible) object for that object ID.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 8 [desktop apps only] |
| **Minimum supported server** | Windows Server 2012 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | oleacc.h |
| **Library** | Oleacc.lib |
| **DLL** | Oleacc.dll |

## See also

[IAccessibleWindowlessSite](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessiblewindowlesssite)

[IAccessibleWindowlessSite::ReleaseObjectIdRange](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccessiblewindowlesssite-releaseobjectidrange)

---
