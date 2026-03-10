# get_ContainingGrid

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nf-uiautomationcore-igriditemprovider-get_containinggrid)

# IGridItemProvider::get\_ContainingGrid method (uiautomationcore.h)

Specifies the UI Automation provider that implements [IGridProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-igridprovider)
and represents the container of this cell or item.

This property is read-only.

## Syntax

```
HRESULT get_ContainingGrid(
  IRawElementProviderSimple **pRetVal
);
```

## Parameters

`pRetVal`

## Return value

None

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2003 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |
| **DLL** | Uiautomationcore.dll |

## See also

[IGridItemProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-igriditemprovider)

[UI Automation Providers Overview](/en-us/windows/desktop/WinAuto/uiauto-providersoverview)

---
