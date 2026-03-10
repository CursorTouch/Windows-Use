# ScrollItemPattern_ScrollIntoView

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/nf-uiautomationcoreapi-scrollitempattern_scrollintoview)

# ScrollItemPattern\_ScrollIntoView function (uiautomationcoreapi.h)

**Note**  This function is deprecated. Client applications should use the Microsoft UI Automation Component Object Model (COM) interfaces instead.

Scrolls the content area of a container object in order to display the UI Automation element within the visible region (viewport) of the container.

## Syntax

```
HRESULT ScrollItemPattern_ScrollIntoView(
  [in] HUIAPATTERNOBJECT hobj
);
```

## Parameters

`[in] hobj`

Type: **HUIAPATTERNOBJECT**

The control pattern object.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

Returns S\_OK if successful or an error value otherwise.

## Remarks

This method does not guarantee the position of the UI Automation element
within the visible region (viewport) of the container.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps only] |
| **Minimum supported server** | Windows Server 2003 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationcoreapi.h |
| **Library** | Uiautomationcore.lib |
| **DLL** | Uiautomationcore.dll |

---
