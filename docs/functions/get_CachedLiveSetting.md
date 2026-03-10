# get_CachedLiveSetting

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement2-get_cachedlivesetting)

# IUIAutomationElement2::get\_CachedLiveSetting method (uiautomationclient.h)

Retrieves a cached value that indicates the type of notifications, if any, that the element sends when the content of the element changes.

This property is read-only.

## Syntax

```
HRESULT get_CachedLiveSetting(
  LiveSetting *retVal
);
```

## Parameters

`retVal`

## Return value

None

## Remarks

This property maps to the Accessible Rich Internet Applications (ARIA) **live** property.

The LiveSetting property is supported by provider elements that are part of a live region. When the content of a live region changes, the provider element can raise a notification. A client application determines whether to notify the user of the changes based on the value of the LiveSetting property.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 8 [desktop apps only] |
| **Minimum supported server** | Windows Server 2012 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[CurrentLiveSetting](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement2-get_currentlivesetting)

[IUIAutomationElement2](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationelement2)

[LiveSetting](/en-us/windows/desktop/api/uiautomationcore/ne-uiautomationcore-livesetting)

---
