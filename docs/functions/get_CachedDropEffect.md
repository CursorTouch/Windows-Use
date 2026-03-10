# get_CachedDropEffect

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationdragpattern-get_cacheddropeffect)

# IUIAutomationDragPattern::get\_CachedDropEffect method (uiautomationclient.h)

Retrieves a cached localized string that indicates what happens when the user drops this element as part of a drag-and-drop operation.

This property is read-only.

## Syntax

```
HRESULT get_CachedDropEffect(
  BSTR *retVal
);
```

## Parameters

`retVal`

## Return value

None

## Remarks

In the source-only style of Microsoft UI Automation drag-and-drop, no elements implement the [DropTarget](/en-us/windows/desktop/WinAuto/uiauto-implementingdroptarget) pattern. To find out what effect dropping the dragged element will have, a client can query the [DropEffect](/en-us/windows/desktop/api/uiautomationcore/nf-uiautomationcore-idragprovider-get_dropeffect) property of the dragged element. This property can be a short string such as "move", or a longer one, such as "insert into Main group". The string is always localized.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 8 [desktop apps only] |
| **Minimum supported server** | Windows Server 2012 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[IUIAutomationDragPattern](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationdragpattern)

[IUIAutomationDropTargetPattern::CachedDropTargetEffect](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationdroptargetpattern-get_cacheddroptargeteffect)

[IUIAutomationDropTargetPattern::CurrentDropTargetEffect](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationdroptargetpattern-get_currentdroptargeteffect)

[UI Automation Support for Drag-and-Drop](/en-us/windows/desktop/WinAuto/ui-automation-support-for-drag-and-drop)

---
