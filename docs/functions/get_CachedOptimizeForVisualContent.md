# get_CachedOptimizeForVisualContent

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement2-get_cachedoptimizeforvisualcontent)

# IUIAutomationElement2::get\_CachedOptimizeForVisualContent method (uiautomationclient.h)

Retrieves a cached value that indicates whether the provider exposes only elements that are visible.

This property is read-only.

## Syntax

```
HRESULT get_CachedOptimizeForVisualContent(
  BOOL *retVal
);
```

## Parameters

`retVal`

## Return value

None

## Remarks

A value of TRUE indicates that the provider optimizes for visual content, while FALSE indicates that the provider optimizes for virtual content. For more information, see [Working with Virtualized Items](/en-us/windows/desktop/WinAuto/uiauto-workingwithvirtualizeditems).

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 8 [desktop apps only] |
| **Minimum supported server** | Windows Server 2012 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[Automation Element Property IDs](/en-us/windows/desktop/WinAuto/uiauto-automation-element-propids)

[CurrentOptimizeForVisualContent](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement2-get_currentoptimizeforvisualcontent)

[IUIAutomationElement2](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationelement2)

**Reference**

---
