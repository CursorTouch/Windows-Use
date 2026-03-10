# get_Minimum

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nf-uiautomationcore-irangevalueprovider-get_minimum)

# IRangeValueProvider::get\_Minimum method (uiautomationcore.h)

Specifies the minimum range value supported by the control.

This property is read-only.

## Syntax

```
HRESULT get_Minimum(
  double *pRetVal
);
```

## Parameters

`pRetVal`

## Return value

None

## Remarks

This value should be less than [Maximum](nf-uiautomationcore-irangevalueprovider-get_maximum).

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
