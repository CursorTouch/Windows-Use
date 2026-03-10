# UiaEventCallback

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/nc-uiautomationcoreapi-uiaeventcallback)

# UiaEventCallback callback function (uiautomationcoreapi.h)

**Note**  This function is deprecated. Client applications should use the Microsoft UI Automation Component Object Model (COM) interfaces instead.

A client-implemented function that is called by UI Automation when an event is raised that the client has subscribed to.

## Syntax

```
UiaEventCallback Uiaeventcallback;

void Uiaeventcallback(
  [in] UiaEventArgs *pArgs,
  [in] SAFEARRAY *pRequestedData,
  [in] BSTR pTreeStructure
)
{...}
```

## Parameters

`[in] pArgs`

Type: **[UiaEventArgs](/en-us/windows/desktop/api/uiautomationcoreapi/ns-uiautomationcoreapi-uiaeventargs)\***

The address of a [UiaEventArgs](/en-us/windows/desktop/api/uiautomationcoreapi/ns-uiautomationcoreapi-uiaeventargs) structure that contains the event arguments.

`[in] pRequestedData`

Type: **[SAFEARRAY](/en-us/windows/win32/api/oaidl/ns-oaidl-safearray)\***

A [SAFEARRAY](/en-us/windows/win32/api/oaidl/ns-oaidl-safearray) that contains data associated with the event.

`[in] pTreeStructure`

Type: **BSTR**

A string that contains the structure of the tree associated with the event, if the event is associated with a set of nodes. See Remarks.

## Return value

None

## Remarks

This function is passed to [UiaAddEvent](/en-us/windows/desktop/api/uiautomationcoreapi/nf-uiautomationcoreapi-uiaaddevent) and [UiaRemoveEvent](/en-us/windows/desktop/api/uiautomationcoreapi/nf-uiautomationcoreapi-uiaremoveevent).

The tree structure is described by a string where every character is either "p" or ")". The first character in the string always represents the root node. The string is **NULL** if no elements are returned by the function.

A "p" represents a node (UI Automation element). When one "p" directly follows another, the second node is a child of the first. A ")" represents a step back up the tree. For example, "pp)p" represents a node followed by two child nodes that are siblings of one another. In "pp))p", the last node is a sibling of the first one.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps only] |
| **Minimum supported server** | Windows Server 2003 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationcoreapi.h |

---
