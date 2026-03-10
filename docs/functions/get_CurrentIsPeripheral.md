# get_CurrentIsPeripheral

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement3-get_currentisperipheral)

# IUIAutomationElement3::get\_CurrentIsPeripheral method (uiautomationclient.h)

Retrieves the current peripheral UI indicator for the element.

This property is read-only.

## Syntax

```
HRESULT get_CurrentIsPeripheral(
  BOOL *retVal
);
```

## Parameters

`retVal`

## Return value

None

## Remarks

When the **IsPeripheral** property is **TRUE**, a client application can't assume that focus was taken by the element even if it's currently keyboard-interactive.

This property is relevant for these control types:

* **UIA\_GroupControlTypeId**
* **UIA\_MenuControlTypeId**
* **UIA\_PaneControlTypeId**
* **UIA\_ToolBarControlTypeId**
* **UIA\_ToolTipControlTypeId**
* **UIA\_WindowControlTypeId**
* **UIA\_CustomControlTypeId**

The appearance of peripheral UI often triggers one of these events, if the peripheral UI supports one of the relevant patterns:

* **WindowOpened** (**UIA\_Window\_WindowOpenedEventId**)
* **MenuOpened** (**UIA\_MenuOpenedEventId**)
* **ToolTipOpened** (**UIA\_ToolTipOpenedEventId**)

When client applications that are assistive technologies handle one of these events, the client should check the value of **CurrentIsPeripheral**. If the value is **TRUE**, the client may need to provide an alternative representation of the peripheral UI that the user can reach with a single action, because the client can't use changed focus as an indicator of new UI or a UI of interest. The peripheral UI won't otherwise exist in the control view, tab sequence and so on. A client is guaranteed that only one peripheral UI item exists in the overall tree at any one time, opening another would close the first one automatically.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 8.1 [desktop apps only] |
| **Minimum supported server** | Windows Server 2012 R2 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[IUIAutomationElement3](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationelement3)

**Reference**

---
