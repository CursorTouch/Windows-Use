# get_Maximum

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nf-uiautomationcore-irangevalueprovider-get_maximum)

# IRangeValueProvider::get\_Maximum method (uiautomationcore.h)

Specifies the maximum range value supported by the control.

This property is read-only.

## Syntax

```
HRESULT get_Maximum(
  double *pRetVal
);
```

## Parameters

`pRetVal`

## Return value

None

## Remarks

This value should be greater than [Minimum](nf-uiautomationcore-irangevalueprovider-get_minimum).

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2003 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |
| **DLL** | Uiautomationcore.dll |

## See also

[IRangeValueProvider interface](nn-uiautomationcore-irangevalueprovider), [UI Automation Providers Overview](/en-us/windows/desktop/WinAuto/uiauto-providersoverview)

---
