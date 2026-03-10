# LookupMnemonicTerm

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/msaatext/nf-msaatext-iaccdictionary-lookupmnemonicterm)

# IAccDictionary::LookupMnemonicTerm method (msaatext.h)

Clients call the **IAccDictionary::LookupMnemonicTerm** method to find the property for a given mnemonic string.

**Note**  Active Accessibility Text Services is deprecated. Please see
[Microsoft Windows Text Services Framework](/en-us/windows/win32/tsf/text-services-framework) for more information on advanced text input and natural language technologies.

## Syntax

```
HRESULT LookupMnemonicTerm(
  [in]  BSTR bstrMnemonic,
  [out] GUID *pTerm
);
```

## Parameters

`[in] bstrMnemonic`

Type: **BSTR**

A non-localized mnemonic string for a property.

`[out] pTerm`

Type: **GUID\***

A GUID representing the property in *bstrMnemonic*.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If successful, returns S\_OK.

## Remarks

If the *bstrMnemonic* parameter is not found in the dictionary, then *pTerm* will be **NULL**.

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
