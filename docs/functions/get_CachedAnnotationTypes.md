# get_CachedAnnotationTypes

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement4-get_cachedannotationtypes)

# IUIAutomationElement4::get\_CachedAnnotationTypes method (uiautomationclient.h)

Returns the cached list of annotation types associated with this element, such as comment, header, footer, and so on.

This property is read-only.

## Syntax

```
HRESULT get_CachedAnnotationTypes(
  SAFEARRAY **retVal
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

[CurrentAnnotationTypes](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement4-get_currentannotationtypes)

[IUIAutomationElement4](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationelement4)

---
