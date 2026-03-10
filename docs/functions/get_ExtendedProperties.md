# get_ExtendedProperties

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nf-uiautomationcore-istylesprovider-get_extendedproperties)

# IStylesProvider::get\_ExtendedProperties method (uiautomationcore.h)

Contains additional properties that are not included in this control pattern, but that provide information about the document content that might be useful to the user.

This property is read-only.

## Syntax

```
HRESULT get_ExtendedProperties(
  BSTR *retVal
);
```

## Parameters

`retVal`

## Return value

None

## Remarks

The extended properties must be localized because they are intended to be consumed by the user.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 8 [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2012 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[IStylesProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-istylesprovider)

---
