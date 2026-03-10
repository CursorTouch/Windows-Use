# Realize

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nf-uiautomationcore-ivirtualizeditemprovider-realize)

# IVirtualizedItemProvider::Realize method (uiautomationcore.h)

Makes the virtual item fully accessible as a UI Automation element.

## Syntax

```
HRESULT Realize();
```

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

When an item is obtained from a virtual list, it is only a placeholder. Use this method to convert it to a full reference to UI Automation element.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[IVirtualizedItemProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-ivirtualizeditemprovider)

---
