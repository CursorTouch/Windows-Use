# HandleStructureChangedEvent

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationstructurechangedeventhandler-handlestructurechangedevent)

# IUIAutomationStructureChangedEventHandler::HandleStructureChangedEvent method (uiautomationclient.h)

Handles an event that is raised when the Microsoft UI Automation tree structure has changed.

## Syntax

```
HRESULT HandleStructureChangedEvent(
  [in] IUIAutomationElement *sender,
  [in] StructureChangeType  changeType,
  [in] SAFEARRAY            *runtimeId
);
```

## Parameters

`[in] sender`

Type: **[IUIAutomationElement](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationelement)\***

A pointer to the element that raised the event.

`[in] changeType`

Type: **[StructureChangeType](/en-us/windows/desktop/api/uiautomationcore/ne-uiautomationcore-structurechangetype)**

A value indicating the type of tree structure change that took place.

`[in] runtimeId`

Type: **[SAFEARRAY](/en-us/windows/win32/api/oaidl/ns-oaidl-safearray)\***

Receives the runtime identifier of the element. This parameter is used only when *changeType* is [StructureChangeType\_ChildRemoved](/en-us/windows/desktop/api/uiautomationcore/ne-uiautomationcore-structurechangetype); it is **NULL** for all other structure-change events.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

This method is implemented by the application to handle events that it has subscribed to by using [AddStructureChangedEventHandler](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomation-addstructurechangedeventhandler)

Adjusting an event handler from within this method is not supported.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[Best Practices for Using Safe Arrays](/en-us/windows/desktop/WinAuto/uiauto-workingwithsafearrays)

[IUIAutomationStructureChangedEventHandler](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationstructurechangedeventhandler)

---
