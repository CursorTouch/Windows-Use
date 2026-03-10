# get_CachedIsDialog

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement9-get_cachedisdialog)

# IUIAutomationElement9::get\_CachedIsDialog method (uiautomationclient.h)

Retrieves the cached dialog window indicator for the element.

This property is read-only.

## Syntax

```
HRESULT get_CachedIsDialog(
  BOOL *retVal
);
```

## Parameters

`retVal`

## Return value

None

## Remarks

When the **CachedIsDialog** property is **TRUE**, a client application can assume the cached window is a dialog.

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
