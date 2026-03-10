# CoalesceEventsOptions

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/ne-uiautomationclient-coalesceeventsoptions)

# CoalesceEventsOptions enumeration (uiautomationclient.h)

Contains possible values for the [CoalesceEvents](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomation6-get_coalesceevents) property, which indicates whether an accessible technology client receives all events, or a subset where duplicate events are detected and filtered.

## Syntax

```
typedef enum CoalesceEventsOptions {
  CoalesceEventsOptions_Disabled = 0,
  CoalesceEventsOptions_Enabled = 0x1
} ;
```

## Constants

|  |
| --- |
| `CoalesceEventsOptions_Disabled` Value: *0* Event coalescing is disabled. |
| `CoalesceEventsOptions_Enabled` Value: *0x1* Event coalescing is enabled. |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 10, version 1607 [desktop apps only] |
| **Minimum supported server** | Windows Server 2016 [desktop apps only] |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[CoalesceEvents](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomation6-get_coalesceevents)

---
