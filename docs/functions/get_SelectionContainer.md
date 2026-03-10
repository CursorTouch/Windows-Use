# get_SelectionContainer

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nf-uiautomationcore-iselectionitemprovider-get_selectioncontainer)

# ISelectionItemProvider::get\_SelectionContainer method (uiautomationcore.h)

Specifies the provider that implements [ISelectionProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-iselectionprovider)
and acts as the container for the calling object.

This property is read-only.

## Syntax

```
HRESULT get_SelectionContainer(
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

## See also

[ISelectionItemProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-iselectionitemprovider)

[UI Automation Providers Overview](/en-us/windows/desktop/WinAuto/uiauto-providersoverview)

---
