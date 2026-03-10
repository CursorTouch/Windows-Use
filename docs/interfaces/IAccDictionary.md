# IAccDictionary

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/msaatext/nn-msaatext-iaccdictionary)

# IAccDictionary interface (msaatext.h)

[Active Accessibility Text Services is deprecated. Please see
[Microsoft Windows Text Services Framework](/en-us/windows/win32/tsf/text-services-framework) for more information on advanced text input and natural language technologies.
]

Exposes methods for string manipulation.

## Inheritance

The **IAccDictionary** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **IAccDictionary** also has these types of members:

## Methods

The **IAccDictionary** interface has these methods.

|  |
| --- |
| [IAccDictionary::ConvertValueToString](nf-msaatext-iaccdictionary-convertvaluetostring)   Clients call the IAccDictionary::ConvertValueToString method to convert a value to a localized string. |
| [IAccDictionary::GetLocalizedString](nf-msaatext-iaccdictionary-getlocalizedstring)   Clients call the IAccDictionary::GetLocalizedString method to get localized strings for all system properties and their values. |
| [IAccDictionary::GetMnemonicString](nf-msaatext-iaccdictionary-getmnemonicstring)   Retrieves a mnemonic string.Note  Active Accessibility Text Services is deprecated. |
| [IAccDictionary::GetParentTerm](nf-msaatext-iaccdictionary-getparentterm)   Clients call the IAccDictionary::GetParentTerm method to navigate through the object hierarchy tree. This method returns the parent object of a specified property. |
| [IAccDictionary::LookupMnemonicTerm](nf-msaatext-iaccdictionary-lookupmnemonicterm)   Clients call the IAccDictionary::LookupMnemonicTerm method to find the property for a given mnemonic string. |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps only] |
| **Minimum supported server** | Windows Server 2003 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | msaatext.h |

---
