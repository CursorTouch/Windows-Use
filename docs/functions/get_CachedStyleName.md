# get_CachedStyleName

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationstylespattern-get_cachedstylename)

# IUIAutomationStylesPattern::get\_CachedStyleName method (uiautomationclient.h)

Retrieves the cached name of the visual style associated with an element in a document.

This property is read-only.

## Syntax

```
HRESULT get_CachedStyleName(
  BSTR *retVal
);
```

## Parameters

`retVal`

## Return value

None

## Remarks

The style name typically indicates the role of the element in the document, such as âHeading 1.â

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 8 [desktop apps only] |
| **Minimum supported server** | Windows Server 2012 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[IUIAutomationStylesPattern](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationstylespattern)

---
