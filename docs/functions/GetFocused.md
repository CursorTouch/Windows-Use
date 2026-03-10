# GetFocused

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/msaatext/nf-msaatext-iaccclientdocmgr-getfocused)

# IAccClientDocMgr::GetFocused method (msaatext.h)

Clients call the **IAccClientDocMgr::GetFocused** method to access a pointer for the document that has focus.

**Note**  Active Accessibility Text Services is deprecated. Please see
[Microsoft Windows Text Services Framework](/en-us/windows/win32/tsf/text-services-framework) for more information on advanced text input and natural language technologies.

## Syntax

```
HRESULT GetFocused(
  [in]  REFIID   riid,
  [out] IUnknown **ppunk
);
```

## Parameters

`[in] riid`

Type: **REFIID**

IID of the document being requested. This is usually IID\_ITextStoreAnchor.

`[out] ppunk`

Type: **IUnknown\***

Interface pointer to the document being requested.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If successful, returns S\_OK.

## Remarks

If the window that has focus is not a document that implements the [ITextStoreACP](/en-us/windows/desktop/api/textstor/nn-textstor-itextstoreacp) interface, *ppunk* will be **NULL**.

Servers might need to poll this method more than once before they receive a document. There can be a limited time lapse (approximately second) between when a document appears in the system and when it is registered with document services.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 2000 Professional [desktop apps only] |
| **Minimum supported server** | Windows Server 2003 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | msaatext.h |
| **DLL** | Msaatext.dll |
| **Redistributable** | Active Accessibility 2.0 RDK on Windows NT 4.0Windows 98 |

---
