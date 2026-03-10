# get_CachedAnnotationObjects

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement4-get_cachedannotationobjects)

# IUIAutomationElement4::get\_CachedAnnotationObjects method (uiautomationclient.h)

Returns the cached list of annotation objects associated with this element, such as comment, header, footer, and so on.

This property is read-only.

## Syntax

```
HRESULT get_CachedAnnotationObjects(
  IUIAutomationElementArray **retVal
);
```

## Parameters

`retVal`

## Return value

None

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 10 [desktop apps only] |
| **Minimum supported server** | Windows Server 2016 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |
| **DLL** | UIAutomationCore.dll |

## See also

[CurrentAnnotationObjects](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement4-get_currentannotationobjects)

[IUIAutomationElement4](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationelement4)

---
