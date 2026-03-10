# Expand

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nf-uiautomationcore-iexpandcollapseprovider-expand)

# IExpandCollapseProvider::Expand method (uiautomationcore.h)

Displays all child nodes, controls, or content of the control.

## Syntax

```
HRESULT Expand();
```

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

This is a blocking method that returns after the control has been expanded.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2003 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |
| **DLL** | Uiautomationcore.dll |

## See also

[IExpandCollapseProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-iexpandcollapseprovider)

[UI Automation Providers Overview](/en-us/windows/desktop/WinAuto/uiauto-providersoverview)

---
