# GetFocusedElement

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomation-getfocusedelement)

# IUIAutomation::GetFocusedElement method (uiautomationclient.h)

Retrieves the UI Automation element that has the input focus.

## Syntax

```
HRESULT GetFocusedElement(
  [out, retval] IUIAutomationElement **element
);
```

## Parameters

`[out, retval] element`

Type: **[IUIAutomationElement](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationelement)\*\***

Receives a pointer to the UI Automation element.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

The **IUIAutomation::GetFocusedElement** method returns the [UIA\_E\_ELEMENTNOTAVAILABLE](/en-us/windows/desktop/WinAuto/uiauto-error-codes) error code if the focused element is already removed by the time the method returns. Clients should handle errors from this method gracefully; for example, by trying the call again.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

---
