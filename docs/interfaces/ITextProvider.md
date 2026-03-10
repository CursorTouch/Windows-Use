# ITextProvider

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nn-uiautomationcore-itextprovider)

# ITextProvider interface (uiautomationcore.h)

Provides access to controls that contain text.

## Inheritance

The **ITextProvider** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **ITextProvider** also has these types of members:

## Methods

The **ITextProvider** interface has these methods.

|  |
| --- |
| [ITextProvider::get\_DocumentRange](nf-uiautomationcore-itextprovider-get_documentrange)   Retrieves a text range that encloses the main text of a document. (ITextProvider.get\_DocumentRange) |
| [ITextProvider::get\_SupportedTextSelection](nf-uiautomationcore-itextprovider-get_supportedtextselection)   Retrieves a value that specifies the type of text selection that is supported by the control. (ITextProvider.get\_SupportedTextSelection) |
| [ITextProvider::GetSelection](nf-uiautomationcore-itextprovider-getselection)   Retrieves a collection of text ranges that represents the currently selected text in a text-based control. (ITextProvider.GetSelection) |
| [ITextProvider::GetVisibleRanges](nf-uiautomationcore-itextprovider-getvisibleranges)   Retrieves an array of disjoint text ranges from a text-based control where each text range represents a contiguous span of visible text. (ITextProvider.GetVisibleRanges) |
| [ITextProvider::RangeFromChild](nf-uiautomationcore-itextprovider-rangefromchild)   Retrieves a text range enclosing a child element such as an image, hyperlink, or other embedded object. |
| [ITextProvider::RangeFromPoint](nf-uiautomationcore-itextprovider-rangefrompoint)   Returns the degenerate (empty) text range nearest to the specified screen coordinates. |

## Remarks

Implemented on a Microsoft UI Automation provider that must support the [Text](/en-us/windows/desktop/WinAuto/uiauto-implementingtextandtextrange) control pattern.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2003 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[ITextProvider2](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-itextprovider2)

[ITextRangeProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-itextrangeprovider)

[UI Automation Providers Overview](/en-us/windows/desktop/WinAuto/uiauto-providersoverview)

---
