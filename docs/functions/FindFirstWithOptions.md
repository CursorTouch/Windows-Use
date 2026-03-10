# FindFirstWithOptions

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement7-findfirstwithoptions)

# IUIAutomationElement7::FindFirstWithOptions method (uiautomationclient.h)

Finds the first matching element in the specified order.

## Syntax

```
HRESULT FindFirstWithOptions(
  [in]           TreeScope              scope,
  [in]           IUIAutomationCondition *condition,
                 TreeTraversalOptions   traversalOptions,
  [in, optional] IUIAutomationElement   *root,
  [out, retval]  IUIAutomationElement   **found
);
```

## Parameters

`[in] scope`

A combination of values specifying the scope of the search.

`[in] condition`

A pointer to a condition that represents the criteria to match.

`traversalOptions`

Enumeration value specifying the tree navigation order.

`[in, optional] root`

A pointer to the element with which to begin the search.

`[out, retval] found`

Receives a pointer to the element. **NULL** is returned if no matching element is found.

## Return value

Returns **S\_OK** if successful, otherwise an **HRESULT** error code.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 10, version 1703 [desktop apps only] |
| **Minimum supported server** | Windows Server 2016 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |
| **DLL** | UIAutomationCore.dll |

## See also

[IUIAutomationElement7](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationelement7)

---
