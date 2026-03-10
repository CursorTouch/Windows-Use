# Scroll

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nf-uiautomationcore-iscrollprovider-scroll)

# IScrollProvider::Scroll method (uiautomationcore.h)

Scrolls the visible region of the content area horizontally and vertically.

## Syntax

```
HRESULT Scroll(
  [in] ScrollAmount horizontalAmount,
  [in] ScrollAmount verticalAmount
);
```

## Parameters

`[in] horizontalAmount`

Type: **[ScrollAmount](/en-us/windows/desktop/api/uiautomationcore/ne-uiautomationcore-scrollamount)**

The horizontal scrolling increment that is specific to the control.

`[in] verticalAmount`

Type: **[ScrollAmount](/en-us/windows/desktop/api/uiautomationcore/ne-uiautomationcore-scrollamount)**

The vertical scrolling increment that is specific to the control.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2003 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

**Conceptual**

[IScrollProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-iscrollprovider)

**Reference**

[UI Automation Providers Overview](/en-us/windows/desktop/WinAuto/uiauto-providersoverview)

---
