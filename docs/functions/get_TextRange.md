# get_TextRange

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationtextchildpattern-get_textrange)

# IUIAutomationTextChildPattern::get\_TextRange method (uiautomationclient.h)

Retrieves a text range that encloses this child element.

This property is read-only.

## Syntax

```
HRESULT get_TextRange(
  IUIAutomationTextRange **range
);
```

## Parameters

`range`

## Return value

None

## Remarks

This property is equivalent to specifying this child element in a call to the [IUIAutomationTextPattern::RangeFromChild](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationtextpattern-rangefromchild) method.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 8 [desktop apps only] |
| **Minimum supported server** | Windows Server 2012 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[IUIAutomationTextChildPattern](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationtextchildpattern)

---
