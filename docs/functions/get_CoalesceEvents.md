# get_CoalesceEvents

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomation6-get_coalesceevents)

# IUIAutomation6::get\_CoalesceEvents method (uiautomationclient.h)

Gets or sets whether an accessible technology client receives all events, or a subset where duplicate events are detected and filtered.

This property is read/write.

## Syntax

```
HRESULT get_CoalesceEvents(
  [in] CoalesceEventsOptions *coalesceEventsOptions
);
```

## Parameters

`[in] coalesceEventsOptions`

Type: [**CoalesceEventsOptions**](ne-uiautomationclient-coalesceeventsoptions)

Value indicating whether events are filtered. The default is [CoalesceEventsOptions\_Disabled](ne-uiautomationclient-coalesceeventsoptions).

## Return value

None

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 10, version 1809 [desktop apps only] |
| **Minimum supported server** | Windows Server, version 1709 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[IUIAutomation6 interface](nn-uiautomationclient-iuiautomation6)

---
