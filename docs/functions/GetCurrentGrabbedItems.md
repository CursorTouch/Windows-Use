# GetCurrentGrabbedItems

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationdragpattern-getcurrentgrabbeditems)

# IUIAutomationDragPattern::GetCurrentGrabbedItems method (uiautomationclient.h)

Retrieves a collection of elements that represent the full set of items that the user is dragging as part of a drag operation.

## Syntax

```
HRESULT GetCurrentGrabbedItems(
  [out, retval, optional] IUIAutomationElementArray **retVal
);
```

## Parameters

`[out, retval, optional] retVal`

Type: **[IAutomationElementArray](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationelementarray)\*\***

The collection of elements that the user is dragging. This property is **NULL** or an empty array if only a single item is being dragged. The default value is an empty array.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

If the user is dragging multiple items, the items are represented by a single master element with an associated set of grabbed elements. The master item fires the appropriate events, to avoid having a large set of duplicate events. The client can query the GrabbedItems property to get the full list of grabbed items.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 8 [desktop apps only] |
| **Minimum supported server** | Windows Server 2012 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[IUIAutomationDragPattern](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationdragpattern)

---
