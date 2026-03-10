# RemoveChangesEventHandler

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomation4-removechangeseventhandler)

# IUIAutomation4::RemoveChangesEventHandler method (uiautomationclient.h)

Removes a changes event handler.

## Syntax

```
HRESULT RemoveChangesEventHandler(
  [in] IUIAutomationElement             *element,
  [in] IUIAutomationChangesEventHandler *handler
);
```

## Parameters

`[in] element`

Type: **[IUIAutomationElement](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationelement)\***

A pointer to the UI Automation element from which to remove the handler.

`[in] handler`

Type: **[IUIAutomationChangesEventHandler](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationchangeseventhandler)\***

A pointer to the interface that was passed to [AddChangesEventHandler](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomation4-addchangeseventhandler).

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 10, version 1607 [desktop apps only] |
| **Minimum supported server** | Windows Server 2016 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[IUIAutomation4](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomation4)

---
