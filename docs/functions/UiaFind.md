# UiaFind

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/nf-uiautomationcoreapi-uiafind)

# UiaFind function (uiautomationcoreapi.h)

**Note**  This function is deprecated. Client applications should use the Microsoft UI Automation Component Object Model (COM) interfaces instead.

Retrieves one or more UI Automation nodes that match the search criteria.

## Syntax

```
HRESULT UiaFind(
  [in]  HUIANODE        hnode,
  [in]  UiaFindParams   *pParams,
  [in]  UiaCacheRequest *pRequest,
  [out] SAFEARRAY       **ppRequestedData,
  [out] SAFEARRAY       **ppOffsets,
  [out] SAFEARRAY       **ppTreeStructures
);
```

## Parameters

`[in] hnode`

Type: **HUIANODE**

The node to use as starting-point of the search.

`[in] pParams`

Type: **[UiaFindParams](/en-us/windows/desktop/api/uiautomationcoreapi/ns-uiautomationcoreapi-uiafindparams)\***

The address of a [UiaFindParams](/en-us/windows/desktop/api/uiautomationcoreapi/ns-uiautomationcoreapi-uiafindparams) structure that contains the search parameters.

`[in] pRequest`

Type: **[UiaCacheRequest](/en-us/windows/desktop/api/uiautomationcoreapi/ns-uiautomationcoreapi-uiacacherequest)\***

The address of a [UiaCacheRequest](/en-us/windows/desktop/api/uiautomationcoreapi/ns-uiautomationcoreapi-uiacacherequest) structure that specifies what information is to be cached.

`[out] ppRequestedData`

Type: **[SAFEARRAY](/en-us/windows/win32/api/oaidl/ns-oaidl-safearray)\*\***

The address of a variable that receives a pointer to a [SAFEARRAY](/en-us/windows/win32/api/oaidl/ns-oaidl-safearray) containing the requested data. This parameter is passed uninitialized. See Remarks.

`[out] ppOffsets`

Type: **[SAFEARRAY](/en-us/windows/win32/api/oaidl/ns-oaidl-safearray)\*\***

The address of a variable that receives a pointer to a SAFEARRAY containing the indexes to the requested data array for where the element subtree starts. This parameter is passed uninitialized.

`[out] ppTreeStructures`

Type: **[SAFEARRAY](/en-us/windows/win32/api/oaidl/ns-oaidl-safearray)\*\***

The address of a variable that receives a pointer to a SAFEARRAY containing the description of the tree structure. This parameter is passed uninitialized. See Remarks.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

Returns S\_OK if successful or an error value otherwise.

## Remarks

The tree structure is described by a string where every character is either "p" or ")".
The first character in the string always represents the root node.
The string is **NULL** if no elements are returned by the function.

A "p" represents a node
(UI Automation element). When one "p" directly follows another, the second node is a child of the first.
A ")" represents a step back up the tree. For example, "pp)p" represents a node followed
by two child nodes that are siblings of one another. In "pp))p", the last node is a sibling of the first one.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps only] |
| **Minimum supported server** | Windows Server 2003 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationcoreapi.h |
| **Library** | Uiautomationcore.lib |
| **DLL** | Uiautomationcore.dll |

---
