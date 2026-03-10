# OnDocumentFocus

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/msaatext/nf-msaatext-iaccserverdocmgr-ondocumentfocus)

# IAccServerDocMgr::OnDocumentFocus method (msaatext.h)

Applications that use Text Services Framework call **IAccServerDocMgr::OnDocumentFocus** to notify the Microsoft Active Accessibility run time when a document gets or loses focus. The store keeps this information so that clients can access the document that has focus.

**Note**  Active Accessibility Text Services is deprecated. Please see
[Microsoft Windows Text Services Framework](/en-us/windows/win32/tsf/text-services-framework) for more information on advanced text input and natural language technologies.

## Syntax

```
HRESULT OnDocumentFocus(
  [in] IUnknown *punk
);
```

## Parameters

`[in] punk`

Type: **IUnknown\***

An interface pointer to the document getting focus.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If successful, returns S\_OK.

## Remarks

This can be null indicating that no document has focus.

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
