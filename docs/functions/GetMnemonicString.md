# GetMnemonicString

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/msaatext/nf-msaatext-iaccdictionary-getmnemonicstring)

# IAccDictionary::GetMnemonicString method (msaatext.h)

Retrieves a mnemonic string.

**Note**  Active Accessibility Text Services is deprecated. Please see
[Microsoft Windows Text Services Framework](/en-us/windows/win32/tsf/text-services-framework) for more information on advanced text input and natural language technologies.

## Syntax

```
HRESULT GetMnemonicString(
  [in]  REFGUID Term,
  [out] BSTR    *pResult
);
```

## Parameters

`[in] Term`

Type: **REFGUID**

A GUID representing a property.

`[out] pResult`

Type: **BSTR\***

A mnemonic string for the property. This string is not localized.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If successful, returns S\_OK.

## Remarks

If the *Term* parameter is not found in the dictionary, then *pResult* will be **NULL**.

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
