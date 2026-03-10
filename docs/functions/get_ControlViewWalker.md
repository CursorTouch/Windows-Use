# get_ControlViewWalker

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomation-get_controlviewwalker)

# IUIAutomation::get\_ControlViewWalker method (uiautomationclient.h)

Retrieves an [IUIAutomationTreeWalker](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationtreewalker) interface used to discover control elements.

This property is read-only.

## Syntax

```
HRESULT get_ControlViewWalker(
  IUIAutomationTreeWalker **walker
);
```

## Parameters

`walker`

## Return value

None

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[ContentViewWalker](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomation-get_contentviewwalker)

[IUIAutomation](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomation)

[IUIAutomationTreeWalker](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationtreewalker)

[RawViewWalker](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomation-get_rawviewwalker)

---
