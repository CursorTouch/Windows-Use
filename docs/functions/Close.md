# Close

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nf-uiautomationcore-iwindowprovider-close)

# IWindowProvider::Close method (uiautomationcore.h)

Attempts to close the window.

## Syntax

```
HRESULT Close();
```

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

**IWindowProvider::Close** must return immediately without blocking.

**IWindowProvider::Close** raises the [UIA\_Window\_WindowClosedEventId](/en-us/windows/desktop/WinAuto/uiauto-event-ids)
event.
If possible, the event should be raised after the control has completed its associated action.

When called on a split pane control, this method will close the pane and remove
the associated split.

This method may also close all other panes depending on implementation.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2003 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[IWindowProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-iwindowprovider)

[UI Automation Providers Overview](/en-us/windows/desktop/WinAuto/uiauto-providersoverview)

---
