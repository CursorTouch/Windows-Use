# get_DropEffect

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nf-uiautomationcore-idragprovider-get_dropeffect)

# IDragProvider::get\_DropEffect method (uiautomationcore.h)

Retrieves a localized string that indicates what happens when this element is dropped as part of a drag-drop operation.

This property is read-only.

## Syntax

```
HRESULT get_DropEffect(
  BSTR *pRetVal
);
```

## Parameters

`pRetVal`

## Return value

None

## Remarks

In the source-only style of UI Automation drag-and-drop, no elements implement the [DropTarget](/en-us/windows/desktop/WinAuto/uiauto-implementingdroptarget) pattern. To find out what effect dropping the dragged element will have, a client can query the **DropEffect** property of the dragged element. This property can be a short string such as "move", or a longer one, such as "insert into Main group". The string is always localized.

If this property changes, the provider must notify clients by calling [UiaRaiseAutomationPropertyChangedEvent](/en-us/windows/desktop/api/uiautomationcoreapi/nf-uiautomationcoreapi-uiaraiseautomationpropertychangedevent) and specifying a property identifier of [UIA\_DragIsGrabbedPropertyId](/en-us/windows/desktop/WinAuto/uiauto-control-pattern-propids) or [UIA\_DragDropEffectPropertyId](/en-us/windows/desktop/WinAuto/uiauto-control-pattern-propids).

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 8 [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2012 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[IDragProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-idragprovider)

---
