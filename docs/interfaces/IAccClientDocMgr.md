# IAccClientDocMgr

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/msaatext/nn-msaatext-iaccclientdocmgr)

# IAccClientDocMgr interface (msaatext.h)

[Active Accessibility Text Services is deprecated. Please see
[Microsoft Windows Text Services Framework](/en-us/windows/win32/tsf/text-services-framework) for more information on advanced text input and natural language technologies.
]

Exposes methods for client applications to retrieve documents.

## Inheritance

The **IAccClientDocMgr** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **IAccClientDocMgr** also has these types of members:

## Methods

The **IAccClientDocMgr** interface has these methods.

|  |
| --- |
| [IAccClientDocMgr::GetDocuments](nf-msaatext-iaccclientdocmgr-getdocuments)   Clients call IAccClientDocMgr::GetDocuments to get a list of all documents that have been registered with the Microsoft Active Accessibility run time. |
| [IAccClientDocMgr::GetFocused](nf-msaatext-iaccclientdocmgr-getfocused)   Clients call the IAccClientDocMgr::GetFocused method to access a pointer for the document that has focus. |
| [IAccClientDocMgr::LookupByHWND](nf-msaatext-iaccclientdocmgr-lookupbyhwnd)   Clients call IAccClientDocMgr::LookupByHWND to get a document by providing the HWND for the document. |
| [IAccClientDocMgr::LookupByPoint](nf-msaatext-iaccclientdocmgr-lookupbypoint)   Clients call IAccClientDocMgr::LookupByPoint to get a document object from a point within the document. |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps only] |
| **Minimum supported server** | Windows Server 2003 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | msaatext.h |

---
