# get_TransactionTimeout

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomation2-get_transactiontimeout)

# IUIAutomation2::get\_TransactionTimeout method (uiautomationclient.h)

Specifies the length of time that UI Automation will wait for a provider to respond to a client request for information about an automation element.

This property is read/write.

## Syntax

```
HRESULT get_TransactionTimeout(
  [out] DWORD *timeout
);
```

## Parameters

`[out] timeout`

Type: **DWORD**

The duration of the time-out period, in milliseconds.

## Return value

None

## Remarks

The default transaction timeout value is 20 seconds. Because some operations require the provider to process hundreds of elements, the provider might need a significant amount of time to return information to the client.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 8 [desktop apps only] |
| **Minimum supported server** | Windows Server 2012 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |
| **DLL** | UIAutomationCore.dll |

## See also

[IUIAutomation2](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomation2)

---
