# UiaAddEvent

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/nf-uiautomationcoreapi-uiaaddevent)

# UiaAddEvent function (uiautomationcoreapi.h)

**Note**  This function is deprecated. Client applications should use the Microsoft UI Automation Component Object Model (COM) interfaces instead.

Adds a listener for events on a node in the UI Automation tree.

## Syntax

```
HRESULT UiaAddEvent(
  [in]  HUIANODE         hnode,
  [in]  EVENTID          eventId,
  [in]  UiaEventCallback *pCallback,
  [in]  TreeScope        scope,
  [in]  PROPERTYID       *pProperties,
  [in]  int              cProperties,
  [in]  UiaCacheRequest  *pRequest,
  [out] HUIAEVENT        *phEvent
);
```

## Parameters

`[in] hnode`

Type: **HUIANODE**

The node to add an event listener to.

`[in] eventId`

Type: **EVENTID**

The identifier of the event to listen for. For a list of event IDs, see [Event Identifiers](/en-us/windows/desktop/WinAuto/uiauto-event-ids).

`[in] pCallback`

Type: **[UiaEventCallback](/en-us/windows/desktop/api/uiautomationcoreapi/nc-uiautomationcoreapi-uiaeventcallback)\***

The address of the application-defined [UiaEventCallback](/en-us/windows/desktop/api/uiautomationcoreapi/nc-uiautomationcoreapi-uiaeventcallback) callback function that is called when the event is raised.

`[in] scope`

Type: **[TreeScope](/en-us/windows/desktop/api/uiautomationclient/ne-uiautomationclient-treescope)\***

A value from the [TreeScope](/en-us/windows/desktop/api/uiautomationclient/ne-uiautomationclient-treescope) enumerated type indicating the scope of events to be handled; that is, whether they are on the element itself,
or on its ancestors and children.

`[in] pProperties`

Type: **PROPERTYID\***

The address of an array that contains the identifiers of the properties to monitor for change events, when *eventId* is the EVENTID derived from AutomationPropertyChanged\_Event\_GUID; otherwise this parameter is **NULL**. For a list of property IDs, see [Property Identifiers](/en-us/windows/desktop/WinAuto/uiauto-entry-propids).

`[in] cProperties`

Type: **int**

The count of elements in the *pProperties* array.

`[in] pRequest`

Type: **[UiaCacheRequest](/en-us/windows/desktop/api/uiautomationcoreapi/ns-uiautomationcoreapi-uiacacherequest)\***

The address of a [UiaCacheRequest](/en-us/windows/desktop/api/uiautomationcoreapi/ns-uiautomationcoreapi-uiacacherequest) structure that defines the cache request in effect for nodes that are returned with events.

`[out] phEvent`

Type: **HUIEVENT\***

When this function returns, contains
a pointer to the event that is added.
This parameter is passed uninitialized.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

Returns S\_OK if successful or an error value otherwise.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps only] |
| **Minimum supported server** | Windows Server 2003 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationcoreapi.h |
| **Library** | Uiautomationcore.lib |
| **DLL** | Uiautomationcore.dll |

## See also

[UiaLookupId](/en-us/windows/desktop/api/uiautomationcoreapi/nf-uiautomationcoreapi-uialookupid)

---
