# get_ConnectionRecoveryBehavior

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomation6-get_connectionrecoverybehavior)

# IUIAutomation6::get\_ConnectionRecoveryBehavior method (uiautomationclient.h)

Indicates whether an accessible technology client adjusts provider request timeouts when the provider is non-responsive.

This property is read/write.

## Syntax

```
HRESULT get_ConnectionRecoveryBehavior(
  [in] ConnectionRecoveryBehaviorOptions *connectionRecoveryBehaviorOptions
);
```

## Parameters

`[in] connectionRecoveryBehaviorOptions`

Type: [**ConnectionRecoveryBehaviorOptions**](ne-uiautomationclient-connectionrecoverybehavioroptions)

Value indicating whether provider request timeouts are adjusted. The default is [ConnectionRecoveryBehaviorOptions\_Disabled](ne-uiautomationclient-connectionrecoverybehavioroptions).

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
