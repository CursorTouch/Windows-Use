# get_StyleName

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nf-uiautomationcore-istylesprovider-get_stylename)

# IStylesProvider::get\_StyleName method (uiautomationcore.h)

Specifies the name of the visual style of an element in a document.

This property is read-only.

## Syntax

```
HRESULT get_StyleName(
  BSTR *retVal
);
```

## Parameters

`retVal`

## Return value

None

## Remarks

The style name typically indicates the role of the element in the document, such as "Heading 1."

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
