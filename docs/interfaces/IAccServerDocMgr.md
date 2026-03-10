# IAccServerDocMgr

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/msaatext/nn-msaatext-iaccserverdocmgr)

# IAccServerDocMgr interface (msaatext.h)

[Active Accessibility Text Services is deprecated. Please see
[Microsoft Windows Text Services Framework](/en-us/windows/win32/tsf/text-services-framework) for more information on advanced text input and natural language technologies.
]

Exposes methods that make documents accessible to client applications.

## Inheritance

The **IAccServerDocMgr** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **IAccServerDocMgr** also has these types of members:

## Methods

The **IAccServerDocMgr** interface has these methods.

|  |
| --- |
| [IAccServerDocMgr::NewDocument](nf-msaatext-iaccserverdocmgr-newdocument)   Server applications call the IAccServerDocMgr::NewDocument method when it is available. The adapter creates a wrapped document and registers it with the store, so clients can access information about the text in the document. |
| [IAccServerDocMgr::OnDocumentFocus](nf-msaatext-iaccserverdocmgr-ondocumentfocus)   Applications that use Text Services Framework call IAccServerDocMgr::OnDocumentFocus to notify the Microsoft Active Accessibility run time when a document gets or loses focus. |
| [IAccServerDocMgr::RevokeDocument](nf-msaatext-iaccserverdocmgr-revokedocument)   Server applications call the IAccServerDocMgr::RevokeDocument method to notify the Microsoft Active Accessibility run time that a document is no longer available. Calling RevokeDocument removes it from the store so that clients cannot see the document. |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps only] |
| **Minimum supported server** | Windows Server 2003 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | msaatext.h |

---
