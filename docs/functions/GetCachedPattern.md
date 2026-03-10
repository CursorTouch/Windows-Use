# GetCachedPattern

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-getcachedpattern)

# IUIAutomationElement::GetCachedPattern method (uiautomationclient.h)

Retrieves from the cache the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface of the specified control pattern of this UI Automation element.

## Syntax

```
HRESULT GetCachedPattern(
  [in]          PATTERNID patternId,
  [out, retval] IUnknown  **patternObject
);
```

## Parameters

`[in] patternId`

Type: **PATTERNID**

The identifier of the control pattern. For a list of control pattern IDs, see [Control Pattern Identifiers](/en-us/windows/desktop/WinAuto/uiauto-controlpattern-ids).

`[out, retval] patternObject`

Type: **[IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown)\*\***

Receives a pointer to an [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

**Conceptual**

[GetCachedPatternAs](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-getcachedpatternas)

[GetCurrentPattern](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-getcurrentpattern)

[IUIAutomationElement](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationelement)

**Reference**

[UI Automation Control Patterns Overview](/en-us/windows/desktop/WinAuto/uiauto-controlpatternsoverview)

---
