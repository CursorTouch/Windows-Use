# get_CachedDropEffects

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationdragpattern-get_cacheddropeffects)

# IUIAutomationDragPattern::get\_CachedDropEffects method (uiautomationclient.h)

Retrieves a cached array of localized strings that enumerate the full set of effects that can happen when the user drops this element as part of a drag-and-drop operation.

This property is read-only.

## Syntax

```
HRESULT get_CachedDropEffects(
  SAFEARRAY **retVal
);
```

## Parameters

`retVal`

## Return value

None

## Remarks

Some drag operations support a set of different drop effects. For example, a drag operation that is initiated with a right-click might display a menu of options for the action that occurs when the element is dropped. In the source-only style of Microsoft UI Automation drag-and-drop, no elements implement the [DropTarget](/en-us/windows/desktop/WinAuto/uiauto-implementingdroptarget) pattern. To find out the set of effects that can happen when the grabbed element is dropped, a client can query the [DropEffects](/en-us/windows/desktop/api/uiautomationcore/nf-uiautomationcore-idragprovider-get_dropeffects) property of the dragged element. This property can contain short strings such as "move", or longer ones such as "insert into Main group". The strings are always localized.

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
