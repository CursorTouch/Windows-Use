# NewDocument

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/msaatext/nf-msaatext-iaccserverdocmgr-newdocument)

# IAccServerDocMgr::NewDocument method (msaatext.h)

Server applications call the **IAccServerDocMgr::NewDocument** method when it is available. The adapter creates a wrapped document and registers it with the store, so clients can access information about the text in the document.

**Note**  Active Accessibility Text Services is deprecated. Please see
[Microsoft Windows Text Services Framework](/en-us/windows/win32/tsf/text-services-framework) for more information on advanced text input and natural language technologies.

## Syntax

```
HRESULT NewDocument(
  [in] REFIID   riid,
       IUnknown *punk
);
```

## Parameters

`[in] riid`

Type: **REFIID**

IID of the document. This is usually IID\_ITextStoreAnchor.

`punk`

Type: **IUnknown\***

[in, iid\_is(riid)] An interface pointer to the document.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If successful, returns S\_OK.

## Remarks

The server application calls the **IAccServerDocMgr::NewDocument** method to notify the Microsoft Active Accessibility run time that a document is available. Calling **NewDocument** adds the document to the Microsoft Active Accessibility store so that clients can access the document.

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
