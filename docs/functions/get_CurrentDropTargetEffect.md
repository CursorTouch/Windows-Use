# get_CurrentDropTargetEffect

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationdroptargetpattern-get_currentdroptargeteffect)

# IUIAutomationDropTargetPattern::get\_CurrentDropTargetEffect method (uiautomationclient.h)

Retrieves a localized string that describes what happens when the user drops the grabbed element on this drop target.

This property is read-only.

## Syntax

```
HRESULT get_CurrentDropTargetEffect(
  BSTR *retVal
);
```

## Parameters

`retVal`

## Return value

None

## Remarks

This property describes the default effect that happens when the user drops a grabbed element on a target, such as moving or copying the element. This property can be a short string such as "move", or a longer one such as "insert into Main group". The string is always localized.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 8 [desktop apps only] |
| **Minimum supported server** | Windows Server 2012 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[IUIAutomationDropTargetPattern](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationdroptargetpattern)

---
