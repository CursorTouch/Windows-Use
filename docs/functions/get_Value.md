# get_Value

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nf-uiautomationcore-ivalueprovider-get_value)

# IValueProvider::get\_Value method (uiautomationcore.h)

The value of the control.

This property is read-only.

## Syntax

```
HRESULT get_Value(
  BSTR *pRetVal
);
```

## Parameters

`pRetVal`

## Return value

None

## Remarks

Single-line edit controls support programmatic access to their contents by implementing [IValueProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-ivalueprovider) (in addition to [ITextProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-itextprovider)). However, multi-line edit controls do not implement **IValueProvider**.

To retrieve the textual contents of multi-line edit controls, the controls must implement [ITextProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-itextprovider). However, **ITextProvider** does not support setting the value of a control.

[IValueProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-ivalueprovider) does not support the retrieval of formatting information or substring values. Implement [ITextProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-itextprovider) in these scenarios.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2003 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[IValueProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-ivalueprovider)

[UI Automation Providers Overview](/en-us/windows/desktop/WinAuto/uiauto-providersoverview)

---
