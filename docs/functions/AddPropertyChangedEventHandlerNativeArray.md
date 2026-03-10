# AddPropertyChangedEventHandlerNativeArray

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomation-addpropertychangedeventhandlernativearray)

# IUIAutomation::AddPropertyChangedEventHandlerNativeArray method (uiautomationclient.h)

Registers a method that handles a native array of property-changed events.

**Note**  Before implementing an event handler, you should be familiar with the threading issues described in [Understanding Threading Issues](/en-us/windows/desktop/WinAuto/uiauto-threading).

## Syntax

```
HRESULT AddPropertyChangedEventHandlerNativeArray(
  [in] IUIAutomationElement                     *element,
  [in] TreeScope                                scope,
  [in] IUIAutomationCacheRequest                *cacheRequest,
  [in] IUIAutomationPropertyChangedEventHandler *handler,
  [in] PROPERTYID                               *propertyArray,
  [in] int                                      propertyCount
);
```

## Parameters

`[in] element`

Type: **[IUIAutomationElement](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationelement)\***

A pointer to the UI Automation element associated with the event handler.

`[in] scope`

Type: **[TreeScope](/en-us/windows/desktop/api/uiautomationclient/ne-uiautomationclient-treescope)**

The scope of events to be handled; that is, whether they are on the element itself, or on its ancestors and children.

`[in] cacheRequest`

Type: **[IUIAutomationCacheRequest](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationcacherequest)\***

A pointer to a cache request, or **NULL** if no caching is wanted.

`[in] handler`

Type: **[IUIAutomationPropertyChangedEventHandler](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationpropertychangedeventhandler)\***

A pointer to the object that handles the event.

`[in] propertyArray`

Type: **PROPERTYID\***

A pointer to the identifiers of the UI Automation properties of interest. For a list of property IDs, see [Property Identifiers](/en-us/windows/desktop/WinAuto/uiauto-entry-propids).

`[in] propertyCount`

Type: **int**

The number of property identifiers in *propertyArray*.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## example

For code examples that show how to implement interfaces that enable clients to receive and handle Microsoft UI Automation events (including AddPropertyChangedEventHandlerNativeArray), see [How to Implement Event Handlers](/en-us/windows/win32/winauto/uiauto-howto-implement-event-handlers).

## Remarks

The UI item specified by *element* might not support the properties specified by the *propertyArray* parameter.

This method serves the same purpose as [IUIAutomation::AddPropertyChangedEventHandler](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomation-addpropertychangedeventhandler), but takes a normal array of property identifiers instead of a SAFEARRAY.

A UI Automation client should not use multiple threads to add or remove event handlers. Unexpected behavior can result if one event handler is being added or removed while another is being added or removed in the same client process.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[AddPropertyChangedEventHandler](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomation-addpropertychangedeventhandler)

[Caching UI Automation Properties and Control Patterns](/en-us/windows/desktop/WinAuto/uiauto-cachingforclients)

**Conceptual**

[IUIAutomation](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomation)

**Reference**

[RemoveAllEventHandlers](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomation-removealleventhandlers)

[RemovePropertyChangedEventHandler](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomation-removepropertychangedeventhandler)

[Subscribing to UI Automation Events](/en-us/windows/desktop/WinAuto/uiauto-eventsforclients)

[Understanding Threading Issues](/en-us/windows/desktop/WinAuto/uiauto-threading)

---
