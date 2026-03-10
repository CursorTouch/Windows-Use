# get_RawViewWalker

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomation-get_rawviewwalker)

# IUIAutomation::get\_RawViewWalker method (uiautomationclient.h)

Retrieves a tree walker object used to traverse an unfiltered view of the Microsoft UI Automation tree.

This property is read-only.

## Syntax

```
HRESULT get_RawViewWalker(
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

[ControlViewWalker](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomation-get_controlviewwalker)

[IUIAutomation](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomation)

**Reference**

---
