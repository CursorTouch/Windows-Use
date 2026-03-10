# ITextRangeProvider

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nn-uiautomationcore-itextrangeprovider)

# ITextRangeProvider interface (uiautomationcore.h)

Provides access to
a span of continuous text in a text container that implements [ITextProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-itextprovider) or [ITextProvider2](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-itextprovider2).

## Inheritance

The **ITextRangeProvider** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **ITextRangeProvider** also has these types of members:

## Methods

The **ITextRangeProvider** interface has these methods.

|  |
| --- |
| [ITextRangeProvider::AddToSelection](nf-uiautomationcore-itextrangeprovider-addtoselection)   Adds the text range to the collection of selected text ranges in a control that supports multiple, disjoint spans of selected text. (ITextRangeProvider.AddToSelection) |
| [ITextRangeProvider::Clone](nf-uiautomationcore-itextrangeprovider-clone)   Returns a new ITextRangeProvider identical to the original ITextRangeProvider and inheriting all properties of the original. |
| [ITextRangeProvider::Compare](nf-uiautomationcore-itextrangeprovider-compare)   Retrieves a value that specifies whether this text range has the same endpoints as another text range. (ITextRangeProvider.Compare) |
| [ITextRangeProvider::CompareEndpoints](nf-uiautomationcore-itextrangeprovider-compareendpoints)   Returns a value that specifies whether two text ranges have identical endpoints. |
| [ITextRangeProvider::ExpandToEnclosingUnit](nf-uiautomationcore-itextrangeprovider-expandtoenclosingunit)   Normalizes the text range by the specified text unit. The range is expanded if it is smaller than the specified unit, or shortened if it is longer than the specified unit. (ITextRangeProvider.ExpandToEnclosingUnit) |
| [ITextRangeProvider::FindAttribute](nf-uiautomationcore-itextrangeprovider-findattribute)   Returns a text range subset that has the specified text attribute value. |
| [ITextRangeProvider::FindText](nf-uiautomationcore-itextrangeprovider-findtext)   Returns a text range subset that contains the specified text. |
| [ITextRangeProvider::GetAttributeValue](nf-uiautomationcore-itextrangeprovider-getattributevalue)   Retrieves the value of the specified text attribute across the text range. |
| [ITextRangeProvider::GetBoundingRectangles](nf-uiautomationcore-itextrangeprovider-getboundingrectangles)   Retrieves a collection of bounding rectangles for each fully or partially visible line of text in a text range. (ITextRangeProvider.GetBoundingRectangles) |
| [ITextRangeProvider::GetChildren](nf-uiautomationcore-itextrangeprovider-getchildren)   Retrieves a collection of all embedded objects that fall within the text range. (ITextRangeProvider.GetChildren) |
| [ITextRangeProvider::GetEnclosingElement](nf-uiautomationcore-itextrangeprovider-getenclosingelement)   Returns the innermost element that encloses the text range. |
| [ITextRangeProvider::GetText](nf-uiautomationcore-itextrangeprovider-gettext)   Retrieves the plain text of the range. |
| [ITextRangeProvider::Move](nf-uiautomationcore-itextrangeprovider-move)   Moves the text range forward or backward by the specified number of text units. |
| [ITextRangeProvider::MoveEndpointByRange](nf-uiautomationcore-itextrangeprovider-moveendpointbyrange)   Moves one endpoint of the current text range to the specified endpoint of a second text range. (ITextRangeProvider.MoveEndpointByRange) |
| [ITextRangeProvider::MoveEndpointByUnit](nf-uiautomationcore-itextrangeprovider-moveendpointbyunit)   Moves one endpoint of the text range the specified number of TextUnit units within the document range. |
| [ITextRangeProvider::RemoveFromSelection](nf-uiautomationcore-itextrangeprovider-removefromselection)   Removes the text range from the collection of selected text ranges in a control that supports multiple, disjoint spans of selected text. |
| [ITextRangeProvider::ScrollIntoView](nf-uiautomationcore-itextrangeprovider-scrollintoview)   Causes the text control to scroll vertically until the text range is visible in the viewport. |
| [ITextRangeProvider::Select](nf-uiautomationcore-itextrangeprovider-select)   Selects the span of text that corresponds to this text range, and removes any previous selection. (ITextRangeProvider.Select) |

## Remarks

A range can represent an insertion point, a portion of text, or all of the text in a container.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2003 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

**Conceptual**

[ITextProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-itextprovider)

**Reference**

[UI Automation Providers Overview](/en-us/windows/desktop/WinAuto/uiauto-providersoverview)

---
