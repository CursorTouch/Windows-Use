# ElementFromPoint

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomation-elementfrompoint)

# IUIAutomation::ElementFromPoint method (uiautomationclient.h)

Retrieves the UI Automation element at the specified point on the desktop.

## Syntax

```
HRESULT ElementFromPoint(
  [in]          POINT                pt,
  [out, retval] IUIAutomationElement **element
);
```

## Parameters

`[in] pt`

Type: **[POINT](/en-us/windows/win32/api/windef/ns-windef-point)**

The desktop coordinates of the UI Automation element.

`[out, retval] element`

Type: **[IUIAutomationElement](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationelement)\*\***

Receives a pointer to the UI Automation element.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

The **IUIAutomation::ElementFromPoint** method returns the [UIA\_E\_ELEMENTNOTAVAILABLE](/en-us/windows/desktop/WinAuto/uiauto-error-codes) error code if the element under the point is already removed by the time the method returns. Clients should handle errors from this method gracefully; for example, by trying the call again.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[IUIAutomation](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomation)

[IUIAutomation::ElementFromPointBuildCache](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomation-elementfrompointbuildcache)

---
