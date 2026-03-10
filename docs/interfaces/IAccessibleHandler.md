# IAccessibleHandler

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/oleacc/nn-oleacc-iaccessiblehandler)

# IAccessibleHandler interface (oleacc.h)

[**IAccessibleHandler** is deprecated and should not be used.]

Exposes a method that retrieves an accessible element from an object ID.

## Inheritance

The **IAccessibleHandler** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **IAccessibleHandler** also has these types of members:

## Methods

The **IAccessibleHandler** interface has these methods.

|  |
| --- |
| [IAccessibleHandler::AccessibleObjectFromID](nf-oleacc-iaccessiblehandler-accessibleobjectfromid)   The AccessibleObjectFromID method retrieves an IAccessibleinterface pointer for the interface associated with the given object ID. Oleacc.dll uses this method to obtain an IAccessible interface pointer for proxies that are supplied by other code. |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps only] |
| **Minimum supported server** | Windows Server 2003 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | oleacc.h |

---
