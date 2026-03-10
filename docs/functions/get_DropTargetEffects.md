# get_DropTargetEffects

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nf-uiautomationcore-idroptargetprovider-get_droptargeteffects)

# IDropTargetProvider::get\_DropTargetEffects method (uiautomationcore.h)

Retrieves an array of localized strings that enumerate the full set of effects that can happen when the user drops a grabbed element on this drop target as part of a drag-and-drop operation.

This property is read-only.

## Syntax

```
HRESULT get_DropTargetEffects(
  SAFEARRAY **pRetVal
);
```

## Parameters

`pRetVal`

## Return value

None

## Remarks

Some drag operations support a set of different drop effects. For example, a drag operation that is initiated with a right-click might display a menu of options for the action that occurs when the element is dropped. To find out the set of effects that can happen when the grabbed element is dropped, a client can query the [DropEffects](/en-us/windows/desktop/api/uiautomationcore/nf-uiautomationcore-idragprovider-get_dropeffects) property of the dragged element. This property can contain short strings such as "move", or longer ones such as "insert into Main group". The strings are always localized.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 8 [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2012 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[IDropTargetProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-idroptargetprovider)

---
