# IUIAutomationTextRange

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nn-uiautomationclient-iuiautomationtextrange)

# IUIAutomationTextRange interface (uiautomationclient.h)

Provides access to a span of continuous text in a container that supports the [IUIAutomationTextPattern](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationtextpattern) interface. Client applications can use the **IUIAutomationTextRange** interface to select, compare, and retrieve embedded objects from the text span. The interface uses two endpoints to delimit where the text span starts and ends. Disjoint spans of text are represented by an [IUIAutomationTextRangeArray](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationtextrangearray) interface.

## Inheritance

The **IUIAutomationTextRange** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **IUIAutomationTextRange** also has these types of members:

## Methods

The **IUIAutomationTextRange** interface has these methods.

|  |
| --- |
| [IUIAutomationTextRange::AddToSelection](nf-uiautomationclient-iuiautomationtextrange-addtoselection)   Adds the text range to the collection of selected text ranges in a control that supports multiple, disjoint spans of selected text. (IUIAutomationTextRange.AddToSelection) |
| [IUIAutomationTextRange::Clone](nf-uiautomationclient-iuiautomationtextrange-clone)   Retrieves a new IUIAutomationTextRange identical to the original and inheriting all properties of the original. |
| [IUIAutomationTextRange::Compare](nf-uiautomationclient-iuiautomationtextrange-compare)   Retrieves a value that specifies whether this text range has the same endpoints as another text range. (IUIAutomationTextRange.Compare) |
| [IUIAutomationTextRange::CompareEndpoints](nf-uiautomationclient-iuiautomationtextrange-compareendpoints)   Retrieves a value that specifies whether the start or end endpoint of this text range is the same as the start or end endpoint of another text range. |
| [IUIAutomationTextRange::ExpandToEnclosingUnit](nf-uiautomationclient-iuiautomationtextrange-expandtoenclosingunit)   Normalizes the text range by the specified text unit. The range is expanded if it is smaller than the specified unit, or shortened if it is longer than the specified unit. (IUIAutomationTextRange.ExpandToEnclosingUnit) |
| [IUIAutomationTextRange::FindAttribute](nf-uiautomationclient-iuiautomationtextrange-findattribute)   Retrieves a text range subset that has the specified text attribute value. |
| [IUIAutomationTextRange::FindText](nf-uiautomationclient-iuiautomationtextrange-findtext)   Retrieves a text range subset that contains the specified text. |
| [IUIAutomationTextRange::GetAttributeValue](nf-uiautomationclient-iuiautomationtextrange-getattributevalue)   Retrieves the value of the specified text attribute across the entire text range. |
| [IUIAutomationTextRange::GetBoundingRectangles](nf-uiautomationclient-iuiautomationtextrange-getboundingrectangles)   Retrieves a collection of bounding rectangles for each fully or partially visible line of text in a text range. (IUIAutomationTextRange.GetBoundingRectangles) |
| [IUIAutomationTextRange::GetChildren](nf-uiautomationclient-iuiautomationtextrange-getchildren)   Retrieves a collection of all embedded objects that fall within the text range. (IUIAutomationTextRange.GetChildren) |
| [IUIAutomationTextRange::GetEnclosingElement](nf-uiautomationclient-iuiautomationtextrange-getenclosingelement)   Returns the innermost UI Automation element that encloses the text range. |
| [IUIAutomationTextRange::GetText](nf-uiautomationclient-iuiautomationtextrange-gettext)   Returns the plain text of the text range. |
| [IUIAutomationTextRange::Move](nf-uiautomationclient-iuiautomationtextrange-move)   Moves the text range forward or backward by the specified number of text units . |
| [IUIAutomationTextRange::MoveEndpointByRange](nf-uiautomationclient-iuiautomationtextrange-moveendpointbyrange)   Moves one endpoint of the current text range to the specified endpoint of a second text range. (IUIAutomationTextRange.MoveEndpointByRange) |
| [IUIAutomationTextRange::MoveEndpointByUnit](nf-uiautomationclient-iuiautomationtextrange-moveendpointbyunit)   Moves one endpoint of the text range the specified number of text units within the document range. |
| [IUIAutomationTextRange::RemoveFromSelection](nf-uiautomationclient-iuiautomationtextrange-removefromselection)   Removes the text range from an existing collection of selected text in a text container that supports multiple, disjoint selections. |
| [IUIAutomationTextRange::ScrollIntoView](nf-uiautomationclient-iuiautomationtextrange-scrollintoview)   Causes the text control to scroll until the text range is visible in the viewport. |
| [IUIAutomationTextRange::Select](nf-uiautomationclient-iuiautomationtextrange-select)   Selects the span of text that corresponds to this text range, and removes any previous selection. (IUIAutomationTextRange.Select) |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[Control Pattern Interfaces for Clients](/en-us/windows/desktop/WinAuto/uiauto-client-controlpatterninterfaces)

[UI Automation Support for Textual Content](/en-us/windows/desktop/WinAuto/uiauto-ui-automation-textpattern-overview)

[Using Text Ranges](/en-us/windows/desktop/WinAuto/uiauto-usingtextrangeobjects)

---
