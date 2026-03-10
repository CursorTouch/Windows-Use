# put_ConnectionTimeout

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomation2-put_connectiontimeout)

# IUIAutomation2::put\_ConnectionTimeout method (uiautomationclient.h)

Specifies the length of time that UI Automation will wait for a provider to respond to a client request for an automation element.

This property is read/write.

## Syntax

```
HRESULT put_ConnectionTimeout(
  [in] DWORD timeout
);
```

## Parameters

`[in] timeout`

Type: **DWORD**

The duration of the time-out period, in milliseconds.

## Return value

None

## Remarks

The default connection timeout value is two seconds. A responsive UI Automation provider can typically return an automation element to a client in a short length of time.

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
