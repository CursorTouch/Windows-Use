# ConvertValueToString

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/msaatext/nf-msaatext-iaccdictionary-convertvaluetostring)

# IAccDictionary::ConvertValueToString method (msaatext.h)

Clients call the **IAccDictionary::ConvertValueToString** method to convert a value to a localized string.

**Note**  Active Accessibility Text Services is deprecated. Please see
[Microsoft Windows Text Services Framework](/en-us/windows/win32/tsf/text-services-framework) for more information on advanced text input and natural language technologies.

## Syntax

```
HRESULT ConvertValueToString(
  [in]  REFGUID Term,
  [in]  LCID    lcid,
  [in]  VARIANT varValue,
  [out] BSTR    *pbstrResult,
  [out] LCID    *plcid
);
```

## Parameters

`[in] Term`

Type: **REFGUID**

A GUID that represents a property.

`[in] lcid`

Type: **[LCID](/en-us/windows/desktop/WinProg/windows-data-types)**

The locale of the string to be returned.

`[in] varValue`

Type: **VARIANT**

The value of the item.

`[out] pbstrResult`

Type: **BSTR\***

A pointer to the converted value.

`[out] plcid`

Type: **[LCID](/en-us/windows/desktop/WinProg/windows-data-types)\***

A pointer to the language of the returned string.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If successful, returns S\_OK.

## Remarks

If the *Term* parameter can be true or false, **ConvertValueToString** will return a localized string or **TRUE** or **FALSE**. If the *Term* parameter represents a color, **ConvertValueToString** will return a string for the closest color name. If the *Term* parameter is not found in the dictionary, then *pbstrResult* will be **NULL**.

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
