# ReleaseObjectIdRange

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/oleacc/nf-oleacc-iaccessiblewindowlesssite-releaseobjectidrange)

# IAccessibleWindowlessSite::ReleaseObjectIdRange method (oleacc.h)

Releases an object ID range that was acquired by a previous call to the [IAccessibleWindowlessSite::AcquireObjectIdRange](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccessiblewindowlesssite-acquireobjectidrange) method.

## Syntax

```
HRESULT ReleaseObjectIdRange(
  [in]           long               rangeBase,
  [in, optional] IAccessibleHandler *pRangeOwner
);
```

## Parameters

`[in] rangeBase`

Type: **long**

The first object ID in the range of IDs to be released.

`[in, optional] pRangeOwner`

Type: **[IAccessibleHandler](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessiblehandler)\***

The windowless ActiveX control with which the range was associated when it was acquired.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

To prevent mistakes when releasing object ranges, the system uses the *pControl* parameter to ensure that the range of object IDs being released actually belongs to the specified windowless control.

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

[IAccessibleWindowlessSite::AcquireObjectIdRange](/en-us/windows/desktop/api/oleacc/nf-oleacc-iaccessiblewindowlesssite-acquireobjectidrange)

---
