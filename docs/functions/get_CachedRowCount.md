# get_CachedRowCount

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationgridpattern-get_cachedrowcount)

# IUIAutomationGridPattern::get\_CachedRowCount method (uiautomationclient.h)

Retrieves the cached number of rows in the grid.

This property is read-only.

## Syntax

```
HRESULT get_CachedRowCount(
  int *retVal
);
```

## Parameters

`retVal`

## Return value

None

## Remarks

Hidden rows and columns, depending on the provider implementation, may be loaded in the Microsoft UI Automation tree and will therefore be reflected in the row count and column count properties. If the hidden rows and columns have not yet been loaded they are not counted.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[IUIAutomationGridPattern](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationgridpattern)

---
