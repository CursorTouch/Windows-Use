# get_CachedIsPeripheral

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement3-get_cachedisperipheral)

# IUIAutomationElement3::get\_CachedIsPeripheral method (uiautomationclient.h)

Retrieves the cached peripheral UI indicator for the element. Peripheral UI appears and supports user interaction, but does not take keyboard focus when it appears. Examples of peripheral UI includes popups, flyouts, context menus, or floating notifications.

This property is read-only.

## Syntax

```
HRESULT get_CachedIsPeripheral(
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
