# UiaNavigate

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/nf-uiautomationcoreapi-uianavigate)

# UiaNavigate function (uiautomationcoreapi.h)

**Note**  This function is deprecated. Client applications should use the Microsoft UI Automation Component Object Model (COM) interfaces instead.

Navigates in the UI Automation tree, optionally retrieving cached information.

## Syntax

```
HRESULT UiaNavigate(
  [in]  HUIANODE          hnode,
  [in]  NavigateDirection direction,
  [in]  UiaCondition      *pCondition,
  [in]  UiaCacheRequest   *pRequest,
  [out] SAFEARRAY         **ppRequestedData,
  [out] BSTR              *ppTreeStructure
);
```

## Parameters

`[in] hnode`

Type: **HUIANODE**

The element on which the navigation begins.

`[in] direction`

Type: **[NavigateDirection](/en-us/windows/desktop/api/uiautomationcore/ne-uiautomationcore-navigatedirection)**

A value from the [NavigateDirection](/en-us/windows/desktop/api/uiautomationcore/ne-uiautomationcore-navigatedirection) enumerated type indicating the direction to navigate from *hnode*.

`[in] pCondition`

Type: **[UiaCondition](/en-us/windows/desktop/api/uiautomationcoreapi/ns-uiautomationcoreapi-uiacondition)\***

The address of a [UiaCondition](/en-us/windows/desktop/api/uiautomationcoreapi/ns-uiautomationcoreapi-uiacondition) structure that specifies the condition that the element being navigated to must match. Use this parameter to skip elements that are not of interest.

`[in] pRequest`

Type: **[UiaCacheRequest](/en-us/windows/desktop/api/uiautomationcoreapi/ns-uiautomationcoreapi-uiacacherequest)\***

The address of a [UiaCacheRequest](/en-us/windows/desktop/api/uiautomationcoreapi/ns-uiautomationcoreapi-uiacacherequest) structure that contains a description of the information to be cached.

`[out] ppRequestedData`

Type: **[SAFEARRAY](/en-us/windows/win32/api/oaidl/ns-oaidl-safearray)\*\***

The address of a variable that receives a pointer to a [SAFEARRAY](/en-us/windows/win32/api/oaidl/ns-oaidl-safearray) that contains the requested data. This parameter is passed uninitialized. See Remarks.

`[out] ppTreeStructure`

Type: **BSTR\***

The address of a variable that receives the description of the tree structure.
This parameter is passed uninitialized. See Remarks.

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
