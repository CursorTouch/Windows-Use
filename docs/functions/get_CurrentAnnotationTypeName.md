# get_CurrentAnnotationTypeName

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationannotationpattern-get_currentannotationtypename)

# IUIAutomationAnnotationPattern::get\_CurrentAnnotationTypeName method (uiautomationclient.h)

Retrieves the localized name of this annotation's type.

This property is read-only.

## Syntax

```
HRESULT get_CurrentAnnotationTypeName(
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
| **Minimum supported client** | Windows 8 [desktop apps only] |
| **Minimum supported server** | Windows Server 2012 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[IUIAutomationAnnotationPattern](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationannotationpattern)

---
