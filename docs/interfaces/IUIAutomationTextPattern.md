# IUIAutomationTextPattern

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nn-uiautomationclient-iuiautomationtextpattern)

# IUIAutomationTextPattern interface (uiautomationclient.h)

Provides access to a control that contains text.

## Inheritance

The **IUIAutomationTextPattern** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **IUIAutomationTextPattern** also has these types of members:

## Methods

The **IUIAutomationTextPattern** interface has these methods.

|  |
| --- |
| [IUIAutomationTextPattern::get\_DocumentRange](nf-uiautomationclient-iuiautomationtextpattern-get_documentrange)   Retrieves a text range that encloses the main text of a document. (IUIAutomationTextPattern.get\_DocumentRange) |
| [IUIAutomationTextPattern::get\_SupportedTextSelection](nf-uiautomationclient-iuiautomationtextpattern-get_supportedtextselection)   Retrieves a value that specifies the type of text selection that is supported by the control. (IUIAutomationTextPattern.get\_SupportedTextSelection) |
| [IUIAutomationTextPattern::GetSelection](nf-uiautomationclient-iuiautomationtextpattern-getselection)   Retrieves a collection of text ranges that represents the currently selected text in a text-based control. (IUIAutomationTextPattern.GetSelection) |
| [IUIAutomationTextPattern::GetVisibleRanges](nf-uiautomationclient-iuiautomationtextpattern-getvisibleranges)   Retrieves an array of disjoint text ranges from a text-based control where each text range represents a contiguous span of visible text. (IUIAutomationTextPattern.GetVisibleRanges) |
| [IUIAutomationTextPattern::RangeFromChild](nf-uiautomationclient-iuiautomationtextpattern-rangefromchild)   Retrieves a text range enclosing a child element such as an image, hyperlink, Microsoft Excel spreadsheet, or other embedded object. |
| [IUIAutomationTextPattern::RangeFromPoint](nf-uiautomationclient-iuiautomationtextpattern-rangefrompoint)   Retrieves the degenerate (empty) text range nearest to the specified screen coordinates. (IUIAutomationTextPattern.RangeFromPoint) |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[Control Pattern Interfaces for Clients](/en-us/windows/desktop/WinAuto/uiauto-client-controlpatterninterfaces)

---
