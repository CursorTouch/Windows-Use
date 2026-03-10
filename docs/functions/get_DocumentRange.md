# get_DocumentRange

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nf-uiautomationcore-itextprovider-get_documentrange)

# ITextProvider::get\_DocumentRange method (uiautomationcore.h)

Retrieves a text range that encloses the main text of a document.

This property is read-only.

## Syntax

```
HRESULT get_DocumentRange(
  ITextRangeProvider **pRetVal
);
```

## Parameters

`pRetVal`

## Return value

None

## Remarks

Some auxiliary text such as headers, footnotes, or annotations may not be included.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2003 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[ITextProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-itextprovider)

[ITextRangeProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-itextrangeprovider)

**Reference**

[UI Automation Providers Overview](/en-us/windows/desktop/WinAuto/uiauto-providersoverview)

---
