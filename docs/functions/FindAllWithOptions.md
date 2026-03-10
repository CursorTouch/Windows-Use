# FindAllWithOptions

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement7-findallwithoptions)

# IUIAutomationElement7::FindAllWithOptions method (uiautomationclient.h)

Find all matching elements in the specified order.

## Syntax

```
HRESULT FindAllWithOptions(
                 TreeScope                 scope,
  [in]           IUIAutomationCondition    *condition,
                 TreeTraversalOptions      traversalOptions,
  [in, optional] IUIAutomationElement      *root,
  [out]          IUIAutomationElementArray **found
);
```

## Parameters

`scope`

A combination of values specifying the scope of the search.

`[in] condition`

A pointer to a condition that represents the criteria to match.

`traversalOptions`

Enumeration value specifying the tree navigation order.

`[in, optional] root`

A pointer to the element with which to begin the search.

`[out] found`

Receives a pointer to an array of matching elements. Returns an empty array if no matching element is found.

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
