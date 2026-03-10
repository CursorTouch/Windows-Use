# ConnectionRecoveryBehaviorOptions

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/ne-uiautomationclient-connectionrecoverybehavioroptions)

# ConnectionRecoveryBehaviorOptions enumeration (uiautomationclient.h)

Contains possible values for the [ConnectionRecoveryBehavior](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomation6-get_connectionrecoverybehavior) property, which indicates whether an accessible technology client adjusts provider request timeouts when the provider is non-responsive.

## Syntax

```
typedef enum ConnectionRecoveryBehaviorOptions {
  ConnectionRecoveryBehaviorOptions_Disabled = 0,
  ConnectionRecoveryBehaviorOptions_Enabled = 0x1
} ;
```

## Constants

|  |
| --- |
| `ConnectionRecoveryBehaviorOptions_Disabled` Value: *0* Connection recovery is disabled. |
| `ConnectionRecoveryBehaviorOptions_Enabled` Value: *0x1* Connection recovery is enabled. |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 10, version 1607 [desktop apps only] |
| **Minimum supported server** | Windows Server 2016 [desktop apps only] |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[ConnectionRecoveryBehavior](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomation6-get_connectionrecoverybehavior)

---
