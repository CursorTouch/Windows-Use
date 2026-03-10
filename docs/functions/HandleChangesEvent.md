# HandleChangesEvent

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationchangeseventhandler-handlechangesevent)

# IUIAutomationChangesEventHandler::HandleChangesEvent method (uiautomationclient.h)

Handles one or more Microsoft UI Automation change events.

## Syntax

```
HRESULT HandleChangesEvent(
  [in] IUIAutomationElement *sender,
  [in] UiaChangeInfo        *uiaChanges,
  [in] int                  changesCount
);
```

## Parameters

`[in] sender`

A pointer to the element that raised the event.

`[in] uiaChanges`

A collection of pointers to [UiaChangeInfo](/en-us/windows/desktop/api/uiautomationcore/ns-uiautomationcore-uiachangeinfo) structures.

`[in] changesCount`

The number of changes that occurred. This is the number of [UiaChangeInfo](/en-us/windows/desktop/api/uiautomationcore/ns-uiautomationcore-uiachangeinfo) structures pointed to by the *uiaChanges* parameter.

## Return value

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

This method is implemented by the application to handle events that it has subscribed to by calling [AddChangesEventHandler](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomation4-addchangeseventhandler).

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 10, version 1703 [desktop apps only] |
| **Minimum supported server** | Windows Server 2016 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[IUIAutomationChangesEventHandler](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationchangeseventhandler)

---
