# AddFocusChangedEventHandler

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomation-addfocuschangedeventhandler)

# IUIAutomation::AddFocusChangedEventHandler method (uiautomationclient.h)

Registers a method that handles focus-changed events.

**Note**  Before implementing an event handler, you should be familiar with the threading issues described in [Understanding Threading Issues](/en-us/windows/desktop/WinAuto/uiauto-threading).

## Syntax

```
HRESULT AddFocusChangedEventHandler(
  [in] IUIAutomationCacheRequest             *cacheRequest,
  [in] IUIAutomationFocusChangedEventHandler *handler
);
```

## Parameters

`[in] cacheRequest`

Type: **[IUIAutomationCacheRequest](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationcacherequest)\***

A pointer to a cache request, or **NULL** if no caching is wanted.

`[in] handler`

Type: **[IUIAutomationFocusChangedEventHandler](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationfocuschangedeventhandler)\***

A pointer to the object that handles the event.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

Focus-changed events are system-wide; you cannot set a narrower scope.

A UI Automation client should not use multiple threads to add or remove event handlers. Unexpected behavior can result if one event handler is being added or removed while another is being added or removed in the same client process.

#### Examples

The following example function creates an object that implements [IUIAutomationFocusChangedEventHandler](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationfocuschangedeventhandler) and subscribes to the event by adding the handler.

```
HRESULT AddFocusHandler(IUIAutomation* pAutomation)
{ 
    // CFocusHandler is a class that implements IUIAutomationFocusChangedEventHandler. 
    CFocusHandler* pFocusHandler = new CFocusHandler();
    if (!pFocusHandler)
    {
        return E_OUTOFMEMORY;
    }
    IUIAutomationFocusChangedEventHandler* pHandler;
    pFocusHandler->QueryInterface(IID_IUIAutomationFocusChangedEventHandler, (void**)&pHandler);
    HRESULT hr = pAutomation->AddFocusChangedEventHandler(NULL, pHandler);
    pFocusHandler->Release();
    return hr;
}
```

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[Caching UI Automation Properties and Control Patterns](/en-us/windows/desktop/WinAuto/uiauto-cachingforclients)

**Conceptual**

[IUIAutomation](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomation)

[IUIAutomationFocusChangedEventHandler](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationfocuschangedeventhandler)

**Reference**

[RemoveAllEventHandlers](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomation-removealleventhandlers)

[RemoveFocusChangedEventHandler](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomation-removefocuschangedeventhandler)

[Subscribing to UI Automation Events](/en-us/windows/desktop/WinAuto/uiauto-eventsforclients)

[Understanding Threading Issues](/en-us/windows/desktop/WinAuto/uiauto-threading)

---
