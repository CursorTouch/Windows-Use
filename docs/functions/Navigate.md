# Navigate

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationcustomnavigationpattern-navigate)

# IUIAutomationCustomNavigationPattern::Navigate method (uiautomationclient.h)

Gets the next element in the specified direction within the logical UI tree.

## Syntax

```
HRESULT Navigate(
  [in]          NavigateDirection    direction,
  [out, retval] IUIAutomationElement **pRetVal
);
```

## Parameters

`[in] direction`

The specified direction.

`[out, retval] pRetVal`

The next element as specified by the *direction* parameter.

## Return value

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 10 [desktop apps only] |
| **Minimum supported server** | Windows Server 2016 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[IUIAutomationCustomNavigationPattern](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationcustomnavigationpattern)

---
