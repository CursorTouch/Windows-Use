# GetLocalizedString

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/msaatext/nf-msaatext-iaccdictionary-getlocalizedstring)

# IAccDictionary::GetLocalizedString method (msaatext.h)

Clients call the **IAccDictionary::GetLocalizedString** method to get localized strings for all system properties and their values.

**Note**  Active Accessibility Text Services is deprecated. Please see
[Microsoft Windows Text Services Framework](/en-us/windows/win32/tsf/text-services-framework) for more information on advanced text input and natural language technologies.

## Syntax

```
HRESULT GetLocalizedString(
  [in]  REFGUID Term,
  [in]  LCID    lcid,
  [out] BSTR    *pResult,
  [out] LCID    *plcid
);
```

## Parameters

`[in] Term`

Type: **REFGUID**

A globally unique identifier (GUID) that represents a property.

`[in] lcid`

Type: **[LCID](/en-us/windows/desktop/WinProg/windows-data-types)**

The locale of the string to be returned.

`[out] pResult`

Type: **BSTR\***

A localized string that represents the term.

`[out] plcid`

Type: **[LCID](/en-us/windows/desktop/WinProg/windows-data-types)\***

The language of the returned string.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If successful, returns S\_OK.

## Remarks

This method returns the names of a property in the language specified by *lcid*. If that language is not on the system, Microsoft Active Accessibility finds the best match and returns the string in that language. If the *Term* parameter is not found in the dictionary, the *pResult* will be **NULL**.

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
