# ITextProvider2

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nn-uiautomationcore-itextprovider2)

# ITextProvider2 interface (uiautomationcore.h)

Extends the [ITextProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-itextprovider) interface to enable Microsoft UI Automation providers to expose textual content that is the target of an annotation, and information about a caret that belongs to the provider.

## Inheritance

The **ITextProvider2** interface inherits from [ITextProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-itextprovider). **ITextProvider2** also has these types of members:

## Methods

The **ITextProvider2** interface has these methods.

|  |
| --- |
| [ITextProvider2::GetCaretRange](nf-uiautomationcore-itextprovider2-getcaretrange)   Provides a zero-length text range at the location of the caret that belongs to the text-based control. |
| [ITextProvider2::RangeFromAnnotation](nf-uiautomationcore-itextprovider2-rangefromannotation)   Exposes a text range that contains the text that is the target of the annotation associated with the specified annotation element. |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 8 [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2012 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[Document Control Type](/en-us/windows/desktop/WinAuto/uiauto-supportdocumentcontroltype)

[ITextProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-itextprovider)

[ITextRangeProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-itextrangeprovider)

[UI Automation Providers Overview](/en-us/windows/desktop/WinAuto/uiauto-providersoverview)

[UI Automation Support for Textual Content](/en-us/windows/desktop/WinAuto/uiauto-ui-automation-textpattern-overview)

---
