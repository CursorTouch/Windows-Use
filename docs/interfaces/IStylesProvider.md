# IStylesProvider

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nn-uiautomationcore-istylesprovider)

# IStylesProvider interface (uiautomationcore.h)

Provides access
to the visual styles associated with the content of a document.

## Inheritance

The **IStylesProvider** interface inherits from the IUnknown interface.

## Methods

The **IStylesProvider** interface has these methods.

|  |
| --- |
| [IStylesProvider::get\_ExtendedProperties](nf-uiautomationcore-istylesprovider-get_extendedproperties)   Contains additional properties that are not included in this control pattern, but that provide information about the document content that might be useful to the user. |
| [IStylesProvider::get\_FillColor](nf-uiautomationcore-istylesprovider-get_fillcolor)   Specifies the fill color of an element in a document. |
| [IStylesProvider::get\_FillPatternColor](nf-uiautomationcore-istylesprovider-get_fillpatterncolor)   Specifies the color of the pattern used to fill an element in a document. |
| [IStylesProvider::get\_FillPatternStyle](nf-uiautomationcore-istylesprovider-get_fillpatternstyle)   Specifies the fill pattern style of an element in a document. |
| [IStylesProvider::get\_Shape](nf-uiautomationcore-istylesprovider-get_shape)   Specifies the shape of an element in a document. |
| [IStylesProvider::get\_StyleId](nf-uiautomationcore-istylesprovider-get_styleid)   Identifies the visual style of an element in a document. |
| [IStylesProvider::get\_StyleName](nf-uiautomationcore-istylesprovider-get_stylename)   Specifies the name of the visual style of an element in a document. |

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
