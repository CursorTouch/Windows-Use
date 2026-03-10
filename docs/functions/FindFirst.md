# FindFirst

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-findfirst)

# IUIAutomationElement::FindFirst method (uiautomationclient.h)

Retrieves the first child or descendant element that matches the specified condition.

## Syntax

```
HRESULT FindFirst(
  [in]          TreeScope              scope,
  [in]          IUIAutomationCondition *condition,
  [out, retval] IUIAutomationElement   **found
);
```

## Parameters

`[in] scope`

Type: **[TreeScope](/en-us/windows/desktop/api/uiautomationclient/ne-uiautomationclient-treescope)**

A combination of values specifying the scope of the search.

`[in] condition`

Type: **[IUIAutomationCondition](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationcondition)\***

A pointer to a condition that represents the criteria to match.

`[out, retval] found`

Type: **[IUIAutomationElement](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationelement)\*\***

Receives a pointer to the element. **NULL** is returned if no matching element is found.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

The scope of the search is relative to the element on which the method is called. Elements are returned in the order in which they were encountered in the tree.

This function cannot search for ancestor elements in the Microsoft UI Automation tree; that is, [TreeScope\_Ancestors](/en-us/windows/desktop/api/uiautomationclient/ne-uiautomationclient-treescope) is not a valid value for the *scope* parameter.

When searching for top-level windows on the desktop, be sure to specify [TreeScope\_Children](/en-us/windows/desktop/api/uiautomationclient/ne-uiautomationclient-treescope) in the *scope* parameter, not [TreeScope\_Descendants](/en-us/windows/desktop/api/uiautomationclient/ne-uiautomationclient-treescope). A search through the entire subtree of the desktop could iterate through thousands of items and lead to a stack overflow.

If your client application might try to find elements in its own user interface, you must make all UI Automation calls on a separate thread.

This function ignores elements in the raw tree. Call [FindFirstBuildCache](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-findfirstbuildcache) to search the raw tree by specifying the appropriate [TreeScope](/en-us/windows/desktop/api/uiautomationclient/ne-uiautomationclient-treescope) on the [IUIAutomationCacheRequest](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationcacherequest) passed to that function.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

**Conceptual**

[FindAll](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-findall)

[FindAllBuildCache](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-findallbuildcache)

[FindFirstBuildCache](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-findfirstbuildcache)

[IUIAutomationElement](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationelement)

[Obtaining UI Automation Elements](/en-us/windows/desktop/WinAuto/uiauto-obtainingelements)

**Reference**

---
