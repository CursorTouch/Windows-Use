# NormalizeElement

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationtreewalker-normalizeelement)

# IUIAutomationTreeWalker::NormalizeElement method (uiautomationclient.h)

Retrieves the ancestor element nearest to the specified Microsoft UI Automation element in the tree view.

## Syntax

```
HRESULT NormalizeElement(
  [in]          IUIAutomationElement *element,
  [out, retval] IUIAutomationElement **normalized
);
```

## Parameters

`[in] element`

Type: **[IUIAutomationElement](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationelement)\***

A pointer to the element from which to start the normalization.

`[out, retval] normalized`

Type: **[IUIAutomationElement](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationelement)\*\***

Receives a pointer to the ancestor element nearest to the specified element in the tree view.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

The element is normalized by navigating up the ancestor chain in the tree until an element that satisfies the view condition (specified by a previous call to [IUIAutomationTreeWalker::Condition](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationtreewalker-get_condition)) is reached. But first, the passed element is tested to see if it matches a normalization condition. If so, the passed element is returned, even though it is not an ancestor.

The method returns **UIA\_E\_ELEMENTNOTAVAILABLE** if no matching element has been found.

This method is useful for applications that obtain references to UI Automation elements by hit-testing. The application might want to work only with specific types of elements, and can use **IUIAutomationTreeWalker::Normalize** to make sure that no matter what element is initially retrieved (for example, when a scroll bar gets the input focus), only the element of interest (such as a content element) is ultimately retrieved.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

---
