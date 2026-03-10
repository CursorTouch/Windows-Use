# Collapse

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationexpandcollapsepattern-collapse)

# IUIAutomationExpandCollapsePattern::Collapse method (uiautomationclient.h)

Hides all child nodes, controls, or content of the element.

## Syntax

```
HRESULT Collapse();
```

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

This is a blocking method that returns after the element has been collapsed.

There are cases when a element that is marked as a leaf node might not know whether it has children until either the **IUIAutomationExpandCollapsePattern::Collapse** or the [IUIAutomationExpandCollapsePattern::Expand](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationexpandcollapsepattern-expand) method is called. This behavior is possible with a tree view control that does delayed loading of its child items. For example, Microsoft Windows Explorer might display the expand icon for a node even though there are currently no child items; when the icon is clicked, the control polls for child items, finds none, and removes the expand icon. In these cases clients should listen for a property-changed event on the [IUIAutomationExpandCollapsePattern::CurrentExpandCollapseState](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationexpandcollapsepattern-get_currentexpandcollapsestate) property.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[IUIAutomationExpandCollapsePattern](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationexpandcollapsepattern)

---
