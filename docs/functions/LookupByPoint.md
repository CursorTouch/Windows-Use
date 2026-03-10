# LookupByPoint

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/msaatext/nf-msaatext-iaccclientdocmgr-lookupbypoint)

# IAccClientDocMgr::LookupByPoint method (msaatext.h)

Clients call **IAccClientDocMgr::LookupByPoint** to get a document object from a point within the document.

**Note**  Active Accessibility Text Services is deprecated. Please see
[Microsoft Windows Text Services Framework](/en-us/windows/win32/tsf/text-services-framework) for more information on advanced text input and natural language technologies.

## Syntax

```
HRESULT LookupByPoint(
  [in]  POINT    pt,
  [in]  REFIID   riid,
  [out] IUnknown **ppunk
);
```

## Parameters

`[in] pt`

Type: **POINT**

A point inside the bounding rectangle of the document to be returned.

`[in] riid`

Type: **REFIID**

IID of the document being requested. This is usually IID\_ITextStoreAnchor.

`[out] ppunk`

Type: **IUnknown\***

Interface pointer to the document being requested.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If successful, returns S\_OK.

If not successful, returns the following value or another standard COM error code.

| Error | Description |
| --- | --- |
| **E\_FAIL** | If the value in *pt* does not fall within the bounding rectangle of an active document, then *ppunk* will be **NULL**. |

## Remarks

Servers might need to poll this method more than once before they receive a document. There can be a limited time lapse (approximately second) between when a document appears in the system and when it is registered with document services.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps only] |
| **Minimum supported server** | Windows Server 2003 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | msaatext.h |
| **DLL** | Msaatext.dll |
| **Redistributable** | Active Accessibility 2.0 RDK on Windows NT 4.0 with SP6 and later and Windows 98 |

---
