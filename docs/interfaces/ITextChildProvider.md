# ITextChildProvider

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nn-uiautomationcore-itextchildprovider)

# ITextChildProvider interface (uiautomationcore.h)

Provides access to a text-based control (or an object embedded in text) that is a child or descendant of another text-based control.

## Inheritance

The **ITextChildProvider** interface inherits from the IUnknown interface.

## Methods

The **ITextChildProvider** interface has these methods.

|  |
| --- |
| [ITextChildProvider::get\_TextContainer](nf-uiautomationcore-itextchildprovider-get_textcontainer)   Retrieves this element's nearest ancestor provider that supports the Text control pattern. |
| [ITextChildProvider::get\_TextRange](nf-uiautomationcore-itextchildprovider-get_textrange)   Retrieves a text range that encloses this child element. (ITextChildProvider.get\_TextRange) |

## Remarks

An element that implements the [TextChild control pattern](/en-us/windows/desktop/WinAuto/textchild-control-pattern) must be a child, or descendent, of an element that supports the [Text control pattern](/en-us/windows/desktop/WinAuto/uiauto-implementingtextandtextrange).

It is not required that this element also implement the [Text control pattern](/en-us/windows/desktop/WinAuto/uiauto-implementingtextandtextrange).

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 8 [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2012 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[Text control pattern](/en-us/windows/desktop/WinAuto/uiauto-implementingtextandtextrange), [TextChild control pattern](/en-us/windows/desktop/WinAuto/textchild-control-pattern), [UI Automation Providers Overview](/en-us/windows/desktop/WinAuto/uiauto-providersoverview)

---
