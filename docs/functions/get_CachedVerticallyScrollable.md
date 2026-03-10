# get_CachedVerticallyScrollable

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationscrollpattern-get_cachedverticallyscrollable)

# IUIAutomationScrollPattern::get\_CachedVerticallyScrollable method (uiautomationclient.h)

Retrieves a cached value that indicates whether the element can scroll vertically.

This property is read-only.

## Syntax

```
HRESULT get_CachedVerticallyScrollable(
  BOOL *retVal
);
```

## Parameters

`retVal`

## Return value

None

## Remarks

This property can be dynamic. For example, the content area of the element might not be larger than the current viewable area, meaning that the property is **FALSE**. However, resizing the element or adding child items can increase the bounds of the content area beyond the viewable area, making the property **TRUE**.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[IUIAutomationScrollPattern](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationscrollpattern)

[IUIAutomationScrollPattern::CachedHorizontallyScrollable](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationscrollpattern-get_cachedhorizontallyscrollable)

---
