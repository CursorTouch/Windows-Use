# get_CurrentIsDialog

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement9-get_currentisdialog)

# IUIAutomationElement9::get\_CurrentIsDialog method (uiautomationclient.h)

Retrieves the current dialog window indicator for the element.

This property is read-only.

## Syntax

```
HRESULT get_CurrentIsDialog(
  BOOL *retVal
);
```

## Parameters

`retVal`

## Return value

None

## Remarks

When the **CurrentIsDialog** property is **TRUE**, a client application can assume the current window is a dialog.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 10 Build 20348 |
| **Minimum supported server** | Windows 10 Build 20348 |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h |

## See also

[IUIAutomationElement9](nn-uiautomationclient-iuiautomationelement9)

**Reference**

---
