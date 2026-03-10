# get_IsGrabbed

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nf-uiautomationcore-idragprovider-get_isgrabbed)

# IDragProvider::get\_IsGrabbed method (uiautomationcore.h)

Indicates whether the element has been grabbed as part of a drag-and-drop operation.

This property is read-only.

## Syntax

```
HRESULT get_IsGrabbed(
  BOOL *pRetVal
);
```

## Parameters

`pRetVal`

## Return value

None

## Remarks

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
