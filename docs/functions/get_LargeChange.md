# get_LargeChange

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nf-uiautomationcore-irangevalueprovider-get_largechange)

# IRangeValueProvider::get\_LargeChange method (uiautomationcore.h)

Specifies the value that is added to or subtracted from the [IRangeValueProvider::Value](/en-us/windows/desktop/api/uiautomationcore/nf-uiautomationcore-irangevalueprovider-get_value)
property when a large change is made, such as when the PAGE DOWN key is pressed.

This property is read-only.

## Syntax

```
HRESULT get_LargeChange(
  double *pRetVal
);
```

## Parameters

`pRetVal`

## Return value

None

## Remarks

The LargeChange property can support Not a Number (NaN) value. When returning a NaN value, the provider should return a quiet (non-signaling) NaN to avoid raising an exception if floating-point exceptions are turned on. The following example shows how to create a quiet NaN:

```
ULONGLONG ulNaN = 0xFFFFFFFFFFFFFFFF;
    *pRetVal = *reinterpret_cast<double*>(&ulNaN);
```

Alternatively, you can use the following function from the standard C++ libraries:

```
numeric_limits<double>::quiet_NaN( )
```

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2003 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |
| **DLL** | Uiautomationcore.dll |

## See also

[IRangeValueProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-irangevalueprovider)

[UI Automation Providers Overview](/en-us/windows/desktop/WinAuto/uiauto-providersoverview)

---
