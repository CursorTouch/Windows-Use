# AddActiveTextPositionChangedEventHandler

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationeventhandlergroup-addactivetextpositionchangedeventhandler)

# IUIAutomationEventHandlerGroup::AddActiveTextPositionChangedEventHandler method (uiautomationclient.h)

Registers a method (in an event handler group) that handles when the active text position changes.

**Important**  Microsoft UI Automation clients should use the handler group methods to register event listeners instead of individual event registration methods defined in the various [IUIAutomation](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomation) namespaces.

## Syntax

```
HRESULT AddActiveTextPositionChangedEventHandler(
  [in] TreeScope                                          scope,
  [in] IUIAutomationCacheRequest                          *cacheRequest,
  [in] IUIAutomationActiveTextPositionChangedEventHandler *handler
);
```

## Parameters

`[in] scope`

The scope of events to be handled; that is, whether they are on the element itself, or on its ancestors and descendants.

`[in] cacheRequest`

A pointer to a cache request, or **NULL** if no caching is wanted.

`[in] handler`

A pointer to the object that handles the active text position changed event.

## Return value

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

Before implementing an event handler, you should be familiar with the threading issues described in [Understanding Threading Issues](/en-us/windows/desktop/WinAuto/uiauto-threading).

Active text position is indicated by a navigation event within or between read-only text elements (such as web browsers, Portable Document Format (PDF) documents, or [EPUB](https://en.wikipedia.org/wiki/EPUB) documents) using bookmarks (or fragment identifiers to refer to a location within a resource). Examples include:

* Navigating to a bookmark within the same web page
* Navigating to a bookmark on a different web page
* Activating a link to a different location within the same PDF
* Activating a link to a different location within the same [EPUB](https://en.wikipedia.org/wiki/EPUB)

Use this event handler to sync the visual location of the bookmark/target with the focus location in a read-only text element, which can diverge when using bookmarks or fragment identifiers.

For example, when a same page anchor (`<a href=â#C4â>Jump to Chapter 4</a> ... <h1><a name="C4">Chapter 4</a></h1>`)
is invoked, the visual location is updated, but the UI Automation client remains at the original location. This results in actions such as text reading or move next item commands starting from the original location, not the new location.

Similarly, activating a new page URI (with a fragment identifier: (`<a href=âwww.blah.com#C4â>Jump to Chapter 4</a>`)) loads the new page and jumps to the specified bookmark, but leaves the UI Automation clients at the top of the page.

For editable text elements, such as [Edit](/en-us/windows/desktop/controls/edit-controls) and [Rich Edit](/en-us/windows/desktop/controls/rich-edit-controls) controls, you can listen for a SelectionChanged event.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 10, version 1809 [desktop apps only] |
| **Minimum supported server** | Windows Server, version 1709 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[IUIAutomationEventHandlerGroup](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationeventhandlergroup)

---
