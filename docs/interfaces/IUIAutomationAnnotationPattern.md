# IUIAutomationAnnotationPattern

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nn-uiautomationclient-iuiautomationannotationpattern)

# IUIAutomationAnnotationPattern interface (uiautomationclient.h)

Provides access to the properties of an annotation in a document.

## Inheritance

The **IUIAutomationAnnotationPattern** interface inherits from the IUnknown interface.

## Methods

The **IUIAutomationAnnotationPattern** interface has these methods.

|  |
| --- |
| [IUIAutomationAnnotationPattern::get\_CachedAnnotationTypeId](nf-uiautomationclient-iuiautomationannotationpattern-get_cachedannotationtypeid)   Retrieves a cached value that identifies this annotation's type. |
| [IUIAutomationAnnotationPattern::get\_CachedAnnotationTypeName](nf-uiautomationclient-iuiautomationannotationpattern-get_cachedannotationtypename)   Retrieves the cached localized name of this annotation's type. |
| [IUIAutomationAnnotationPattern::get\_CachedAuthor](nf-uiautomationclient-iuiautomationannotationpattern-get_cachedauthor)   Retrieves the cached name of the annotation author. |
| [IUIAutomationAnnotationPattern::get\_CachedDateTime](nf-uiautomationclient-iuiautomationannotationpattern-get_cacheddatetime)   Retrieves the cached date and time that this annotation was created. |
| [IUIAutomationAnnotationPattern::get\_CachedTarget](nf-uiautomationclient-iuiautomationannotationpattern-get_cachedtarget)   Retrieves the cached element that is being annotated. |
| [IUIAutomationAnnotationPattern::get\_CurrentAnnotationTypeId](nf-uiautomationclient-iuiautomationannotationpattern-get_currentannotationtypeid)   Retrieves a value that identifies the annotation's type. |
| [IUIAutomationAnnotationPattern::get\_CurrentAnnotationTypeName](nf-uiautomationclient-iuiautomationannotationpattern-get_currentannotationtypename)   Retrieves the localized name of this annotation's type. |
| [IUIAutomationAnnotationPattern::get\_CurrentAuthor](nf-uiautomationclient-iuiautomationannotationpattern-get_currentauthor)   Retrieves the name of the annotation author. |
| [IUIAutomationAnnotationPattern::get\_CurrentDateTime](nf-uiautomationclient-iuiautomationannotationpattern-get_currentdatetime)   Retrieves the date and time that this annotation was created. |
| [IUIAutomationAnnotationPattern::get\_CurrentTarget](nf-uiautomationclient-iuiautomationannotationpattern-get_currenttarget)   Retrieves the element that is being annotated. |

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
