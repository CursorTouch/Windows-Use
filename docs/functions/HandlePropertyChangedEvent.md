# HandlePropertyChangedEvent

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationpropertychangedeventhandler-handlepropertychangedevent)

# IUIAutomationPropertyChangedEventHandler::HandlePropertyChangedEvent method (uiautomationclient.h)

Handles a Microsoft UI Automation property-changed event.

## Syntax

```
HRESULT HandlePropertyChangedEvent(
  [in] IUIAutomationElement *sender,
  [in] PROPERTYID           propertyId,
  [in] VARIANT              newValue
);
```

## Parameters

`[in] sender`

Type: **[IUIAutomationElement](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationelement)\***

A pointer to the element that raised the event.

`[in] propertyId`

Type: **PROPERTYID**

The identifier of the property whose value has changed. For a list of property IDs, see [Property Identifiers](/en-us/windows/desktop/WinAuto/uiauto-entry-propids).

`[in] newValue`

Type: **[VARIANT](/en-us/windows/desktop/api/oaidl/ns-oaidl-variant)**

The new property value.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

This method is implemented by the application to handle events that it has subscribed to by using [AddPropertyChangedEventHandler](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomation-addpropertychangedeventhandler).

Adjusting an event handler from within this method is not supported.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

---
