# ShowContextMenu

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement3-showcontextmenu)

# IUIAutomationElement3::ShowContextMenu method (uiautomationclient.h)

Programmatically invokes a context menu on the target element.

## Syntax

```
HRESULT ShowContextMenu();
```

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

This method returns an error code if the context menu could not be invoked. If no context menu is available directly on the element on which it was invoked, calling this method might invoke a context menu on the Microsoft UI Automation parent of the current item.

The context menus themselves fire menu opened / closed events when they are invoked and dismissed.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 8.1 [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2012 R2 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |
| **DLL** | UIAutomationCore.dll |

## See also

[IUIAutomationElement3](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationelement3)

---
