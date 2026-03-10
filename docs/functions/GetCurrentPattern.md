# GetCurrentPattern

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-getcurrentpattern)

# IUIAutomationElement::GetCurrentPattern method (uiautomationclient.h)

Retrieves the [IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown) interface of the specified control pattern on this UI Automation element.

## Syntax

```
HRESULT GetCurrentPattern(
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

## Remarks

This method gets the specified control pattern based on its availability at the time of the call.

For some forms of UI, this method will incur cross-process performance overhead. Applications can reduce overhead by caching control patterns and then retrieving them by using [IUIAutomationElement::GetCachedPattern](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-getcachedpattern).

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

**Conceptual**

[GetCachedPattern](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-getcachedpattern)

[GetCurrentPatternAs](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-getcurrentpatternas)

[IUIAutomationElement](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationelement)

**Reference**

[UI Automation Control Patterns Overview](/en-us/windows/desktop/WinAuto/uiauto-controlpatternsoverview)

---
