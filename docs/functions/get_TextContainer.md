# get_TextContainer

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationtextchildpattern-get_textcontainer)

# IUIAutomationTextChildPattern::get\_TextContainer method (uiautomationclient.h)

Retrieves this element's nearest ancestor element that supports the [Text](/en-us/windows/desktop/WinAuto/uiauto-implementingtextandtextrange) control pattern.

This property is read-only.

## Syntax

```
HRESULT get_TextContainer(
  IUIAutomationElement **container
);
```

## Parameters

`container`

## Return value

None

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
