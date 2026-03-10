# IObjectModelProvider

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nn-uiautomationcore-iobjectmodelprovider)

# IObjectModelProvider interface (uiautomationcore.h)

Provides access to the underlying object model implemented by a control or application. Assistive technology applications can use the object model to directly access the content of the control or application.

## Inheritance

The **IObjectModelProvider** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **IObjectModelProvider** also has these types of members:

## Methods

The **IObjectModelProvider** interface has these methods.

|  |
| --- |
| [IObjectModelProvider::GetUnderlyingObjectModel](nf-uiautomationcore-iobjectmodelprovider-getunderlyingobjectmodel)   Retrieves an interface used to access the underlying object model of the provider. (IObjectModelProvider.GetUnderlyingObjectModel) |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 8 [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2012 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[Control Pattern Interfaces for Providers](/en-us/windows/desktop/WinAuto/uiauto-cpinterfaces)

---
