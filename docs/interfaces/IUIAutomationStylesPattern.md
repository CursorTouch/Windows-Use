# IUIAutomationStylesPattern

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nn-uiautomationclient-iuiautomationstylespattern)

# IUIAutomationStylesPattern interface (uiautomationclient.h)

Enables Microsoft UI Automation clients to retrieve the visual styles associated with an element in a document.

## Inheritance

The **IUIAutomationStylesPattern** interface inherits from the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. **IUIAutomationStylesPattern** also has these types of members:

## Methods

The **IUIAutomationStylesPattern** interface has these methods.

|  |
| --- |
| [IUIAutomationStylesPattern::get\_CachedExtendedProperties](nf-uiautomationclient-iuiautomationstylespattern-get_cachedextendedproperties)   Retrieves a cached localized string that contains the list of extended properties for an element in a document. |
| [IUIAutomationStylesPattern::get\_CachedFillColor](nf-uiautomationclient-iuiautomationstylespattern-get_cachedfillcolor)   Retrieves the cached fill color of an element in a document. |
| [IUIAutomationStylesPattern::get\_CachedFillPatternColor](nf-uiautomationclient-iuiautomationstylespattern-get_cachedfillpatterncolor)   Retrieves the cached color of the pattern used to fill an element in a document. |
| [IUIAutomationStylesPattern::get\_CachedShape](nf-uiautomationclient-iuiautomationstylespattern-get_cachedshape)   Retrieves the cached shape of an element in a document. |
| [IUIAutomationStylesPattern::get\_CachedStyleId](nf-uiautomationclient-iuiautomationstylespattern-get_cachedstyleid)   Retrieves the cached identifier of the visual style associated with an element in a document. |
| [IUIAutomationStylesPattern::get\_CachedStyleName](nf-uiautomationclient-iuiautomationstylespattern-get_cachedstylename)   Retrieves the cached name of the visual style associated with an element in a document. |
| [IUIAutomationStylesPattern::get\_CurrentExtendedProperties](nf-uiautomationclient-iuiautomationstylespattern-get_currentextendedproperties)   Retrieves a localized string that contains the list of extended properties for an element in a document. |
| [IUIAutomationStylesPattern::get\_CurrentFillColor](nf-uiautomationclient-iuiautomationstylespattern-get_currentfillcolor)   Retrieves the fill color of an element in a document. |
| [IUIAutomationStylesPattern::get\_CurrentFillPatternColor](nf-uiautomationclient-iuiautomationstylespattern-get_currentfillpatterncolor)   Retrieves the color of the pattern used to fill an element in a document. |
| [IUIAutomationStylesPattern::get\_CurrentShape](nf-uiautomationclient-iuiautomationstylespattern-get_currentshape)   Retrieves the shape of an element in a document. |
| [IUIAutomationStylesPattern::get\_CurrentStyleId](nf-uiautomationclient-iuiautomationstylespattern-get_currentstyleid)   Retrieves the identifier of the visual style associated with an element in a document. |
| [IUIAutomationStylesPattern::get\_CurrentStyleName](nf-uiautomationclient-iuiautomationstylespattern-get_currentstylename)   Retrieves the name of the visual style associated with an element in a document. |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 8 [desktop apps only] |
| **Minimum supported server** | Windows Server 2012 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[Control Pattern Interfaces for Clients](/en-us/windows/desktop/WinAuto/uiauto-client-controlpatterninterfaces)

---
