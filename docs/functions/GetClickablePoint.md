# GetClickablePoint

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-getclickablepoint)

# IUIAutomationElement::GetClickablePoint method (uiautomationclient.h)

Retrieves a point on the element that can be clicked.

## Syntax

```
HRESULT GetClickablePoint(
  [out]         POINT *clickable,
  [out, retval] BOOL  *gotClickable
);
```

## Parameters

`[out] clickable`

Type: **[POINT](/en-us/windows/win32/api/windef/ns-windef-point)\***

Receives the physical screen coordinates of a point that can be used by a client to click this element.

`[out, retval] gotClickable`

Type: **[BOOL](/en-us/windows/desktop/WinProg/windows-data-types)\***

Receives **TRUE** if a clickable point was retrieved, or **FALSE** otherwise.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

A client application can use this method to simulate clicking the left or right mouse button. For example, to simulate clicking the right mouse button to display the context menu for a control:

* Call the **GetClickablePoint** method to find a clickable point on the control.
* Call the [SendInput](/en-us/windows/desktop/api/winuser/nf-winuser-sendinput) function to send a right-mouse-down, right-mouse-up sequence.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[Automation Element Property IDs](/en-us/windows/desktop/WinAuto/uiauto-automation-element-propids)

[IUIAutomationElement](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationelement)

**Reference**

---
