# Resize

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationtransformpattern-resize)

# IUIAutomationTransformPattern::Resize method (uiautomationclient.h)

Resizes the UI Automation element.

## Syntax

```
HRESULT Resize(
  [in] double width,
  [in] double height
);
```

## Parameters

`[in] width`

Type: **double**

The new width of the window, in pixels.

`[in] height`

Type: **double**

The new height of the window, in pixels.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

When called on a control that supports split panes, this method can have the side effect of resizing other contiguous panes.

An object cannot be moved, resized, or rotated such that its resulting screen location would be completely outside the coordinates of its container and inaccessible to the keyboard or mouse. For example, when a top-level window is moved completely off-screen or a child object is moved outside the boundaries of the container's viewport. In these cases the object is placed as close to the requested screen coordinates as possible with the top or left coordinates overridden to be within the container boundaries.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[CachedCanResize](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationtransformpattern-get_cachedcanresize)

[CurrentCanResize](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationtransformpattern-get_currentcanresize)

[IUIAutomationTransformPattern](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationtransformpattern)

---
