# get_SupportedTextSelection

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nf-uiautomationcore-itextprovider-get_supportedtextselection)

# ITextProvider::get\_SupportedTextSelection method (uiautomationcore.h)

Retrieves a value that specifies the type of text selection that is supported by the control.

This property is read-only.

## Syntax

```
HRESULT get_SupportedTextSelection (SupportedTextSelection *pRetVal);
```

## Parameters

`pRetVal`

## Return value

None

## Remarks

> ### Parameters
>
> `pRetVal` [out]
>
> Type: **[SupportedTextSelection](ne-uiautomationcore-supportedtextselection)\***
>
> When this function returns, contains a pointer to the [SupportedTextSelection](ne-uiautomationcore-supportedtextselection) object.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2003 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[ITextProvider interface](nn-uiautomationcore-itextprovider), [ITextRangeProvider interface](nn-uiautomationcore-itextrangeprovider), [UI Automation Providers Overview](/en-us/windows/desktop/WinAuto/uiauto-providersoverview)

---
