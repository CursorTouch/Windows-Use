# GetParentTerm

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/msaatext/nf-msaatext-iaccdictionary-getparentterm)

# IAccDictionary::GetParentTerm method (msaatext.h)

Clients call the **IAccDictionary::GetParentTerm** method to navigate through the object hierarchy tree. This method returns the parent object of a specified property.

**Note**  Active Accessibility Text Services is deprecated. Please see
[Microsoft Windows Text Services Framework](/en-us/windows/win32/tsf/text-services-framework) for more information on advanced text input and natural language technologies.

## Syntax

```
HRESULT GetParentTerm(
  [in]  REFGUID Term,
  [out] GUID    *pParentTerm
);
```

## Parameters

`[in] Term`

Type: **REFGUID**

A GUID for a property.

`[out] pParentTerm`

Type: **GUID\***

The parent of the property specified in the *Term* parameter.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If successful, returns S\_OK.

## Remarks

If there is not a parent term for *Term*, then *pParentTerm* will point to GUID\_NULL.

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
