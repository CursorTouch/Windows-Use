# RevokeDocument

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/msaatext/nf-msaatext-iaccserverdocmgr-revokedocument)

# IAccServerDocMgr::RevokeDocument method (msaatext.h)

Server applications call the **IAccServerDocMgr::RevokeDocument** method to notify the Microsoft Active Accessibility run time that a document is no longer available. Calling **RevokeDocument** removes it from the store so that clients cannot see the document.

**Note**  Active Accessibility Text Services is deprecated. Please see
[Microsoft Windows Text Services Framework](/en-us/windows/win32/tsf/text-services-framework) for more information on advanced text input and natural language technologies.

## Syntax

```
HRESULT RevokeDocument(
  [in] IUnknown *punk
);
```

## Parameters

`[in] punk`

Type: **IUnknown\***

An interface pointer to the document being revoked.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If successful, returns S\_OK.

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
