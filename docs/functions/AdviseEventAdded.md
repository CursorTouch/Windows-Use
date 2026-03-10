# AdviseEventAdded

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nf-uiautomationcore-irawelementprovideradviseevents-adviseeventadded)

# IRawElementProviderAdviseEvents::AdviseEventAdded method (uiautomationcore.h)

Notifies the Microsoft UI Automation provider when a UI Automation client begins listening for a specific event, including a
property-changed event.

## Syntax

```
HRESULT AdviseEventAdded(
  [in] EVENTID   eventId,
  [in] SAFEARRAY *propertyIDs
);
```

## Parameters

`[in] eventId`

Type: **EVENTID**

The identifier of the event being added. For a list of event IDs, see [Event Identifiers](/en-us/windows/desktop/WinAuto/uiauto-event-ids).

`[in] propertyIDs`

Type: **[SAFEARRAY](/en-us/windows/win32/api/oaidl/ns-oaidl-safearray)\***

A pointer to the identifiers of properties being added, or **NULL** if the event listener
being added is not listening for property events.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

This method enables the provider to reduce overhead by raising only events
that are being listened for.

It is important for UI Automation providers to treat the **IRawElementProviderAdviseEvents::AdviseEventAdded** like the [AddRef](/en-us/windows/desktop/api/unknwn/nf-unknwn-iunknown-addref) method of the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface. As long as **AdviseEventAdded** has been called more times than [AdviseEventRemoved](/en-us/windows/desktop/api/uiautomationcore/nf-uiautomationcore-irawelementprovideradviseevents-adviseeventremoved) for a specific event or property, the provider should continue to raise corresponding events, because some clients are still listening. Alternatively, UI Automation providers can use the [UiaClientsAreListening](/en-us/windows/desktop/api/uiautomationcoreapi/nf-uiautomationcoreapi-uiaclientsarelistening) function to determine if at least one client is listening and, if so, raise all appropriate events.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2003 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[Best Practices for Using Safe Arrays](/en-us/windows/desktop/WinAuto/uiauto-workingwithsafearrays)

**Conceptual**

[IRawElementProviderAdviseEvents](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-irawelementprovideradviseevents)

**Reference**

---
