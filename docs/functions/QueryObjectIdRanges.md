# QueryObjectIdRanges

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/oleacc/nf-oleacc-iaccessiblewindowlesssite-queryobjectidranges)

# IAccessibleWindowlessSite::QueryObjectIdRanges method (oleacc.h)

Retrieves the object ID ranges that a particular windowless Microsoft ActiveX control has reserved.

## Syntax

```
HRESULT QueryObjectIdRanges(
  [in, optional]  IAccessibleHandler *pRangesOwner,
  [out, optional] SAFEARRAY          **psaRanges
);
```

## Parameters

`[in, optional] pRangesOwner`

Type: **[IAccessibleHandler](/en-us/windows/desktop/api/oleacc/nn-oleacc-iaccessiblehandler)\***

The control whose ranges are being queried.

`[out, optional] psaRanges`

Type: **SAFEARRAY\*\***

Receives the array of object ID ranges. The array contains a set of paired integers. For each pair, the first integer is the first object ID in the range, and the second integer is a count of object IDs in the range.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

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

---
