# get_AnnotationTypeName

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nf-uiautomationcore-iannotationprovider-get_annotationtypename)

# IAnnotationProvider::get\_AnnotationTypeName method (uiautomationcore.h)

The name of this annotation type.

This property is read-only.

## Syntax

```
HRESULT get_AnnotationTypeName(
  BSTR *retVal
);
```

## Parameters

`retVal`

## Return value

None

## Remarks

The name of the annotation type can correspond to one of the annotation type identifiers (for example, âCommentâ for [AnnotationType\_Comment](/en-us/windows/desktop/WinAuto/uiauto-annotation-type-identifiers)), but it is not required to.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 8 [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2012 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[IAnnotationProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-iannotationprovider)

---
