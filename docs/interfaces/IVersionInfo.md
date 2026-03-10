# IVersionInfo

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/msaatext/nn-msaatext-iversioninfo)

# IVersionInfo interface (msaatext.h)

[Active Accessibility Text Services is deprecated. Please see
[Microsoft Windows Text Services Framework](/en-us/windows/win32/tsf/text-services-framework) for more information on advanced text input and natural language technologies.
]

Exposes methods that supply version information for accessible elements.

## Inheritance

The **IVersionInfo** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **IVersionInfo** also has these types of members:

## Methods

The **IVersionInfo** interface has these methods.

|  |
| --- |
| [IVersionInfo::GetBuildVersion](nf-msaatext-iversioninfo-getbuildversion)   Clients call IVersionInfo::GetBuildVersion to retrieve build information for a specified component. |
| [IVersionInfo::GetComponentDescription](nf-msaatext-iversioninfo-getcomponentdescription)   Clients call this method to retrieve a description of the component. |
| [IVersionInfo::GetImplementationID](nf-msaatext-iversioninfo-getimplementationid)   Clients call IVersionInfo::GetImplementationID to retrieve a unique identifier for the component. |
| [IVersionInfo::GetInstanceDescription](nf-msaatext-iversioninfo-getinstancedescription)   Clients call this method to retrieve a description of the instance.Note  Active Accessibility Text Services is deprecated. |
| [IVersionInfo::GetSubcomponentCount](nf-msaatext-iversioninfo-getsubcomponentcount)   Clients call IVersionInfo::GetSubcomponentCount to determine the number of subcomponents for which version information is returned. |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps only] |
| **Minimum supported server** | Windows Server 2003 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | msaatext.h |

---
