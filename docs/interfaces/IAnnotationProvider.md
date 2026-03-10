# IAnnotationProvider

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nn-uiautomationcore-iannotationprovider)

# IAnnotationProvider interface (uiautomationcore.h)

Exposes the properties of an annotation in a document.

## Inheritance

The **IAnnotationProvider** interface inherits from the IUnknown interface.

## Methods

The **IAnnotationProvider** interface has these methods.

|  |
| --- |
| [IAnnotationProvider::get\_AnnotationTypeId](nf-uiautomationcore-iannotationprovider-get_annotationtypeid)   The annotation type identifier of this annotation. |
| [IAnnotationProvider::get\_AnnotationTypeName](nf-uiautomationcore-iannotationprovider-get_annotationtypename)   The name of this annotation type. |
| [IAnnotationProvider::get\_Author](nf-uiautomationcore-iannotationprovider-get_author)   The name of the annotation author. |
| [IAnnotationProvider::get\_DateTime](nf-uiautomationcore-iannotationprovider-get_datetime)   The date and time when this annotation was created. |
| [IAnnotationProvider::get\_Target](nf-uiautomationcore-iannotationprovider-get_target)   The UI Automation element that is being annotated. |

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
