# PollForPotentialSupportedPatterns

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomation-pollforpotentialsupportedpatterns)

# IUIAutomation::PollForPotentialSupportedPatterns method (uiautomationclient.h)

Retrieves the control patterns that might be supported on a UI Automation element.

## Syntax

```
HRESULT PollForPotentialSupportedPatterns(
  [in]  IUIAutomationElement *pElement,
  [out] SAFEARRAY            **patternIds,
  [out] SAFEARRAY            **patternNames
);
```

## Parameters

`[in] pElement`

Type: **[IUIAutomationElement](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationelement)\***

The address of the element to poll.

`[out] patternIds`

Type: **SAFEARRAY(int)\*\***

Receives a pointer to an array of control pattern identifiers.

`[out] patternNames`

Type: **SAFEARRAY(BSTR)\*\***

Receives a pointer to an array of control pattern names.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

This method is intended only for use by Microsoft UI Automation tools that need to scan for properties. It is not intended to be used by UI Automation clients.

There is no guarantee that the element will support any particular control pattern when asked for it later.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[Best Practices for Using Safe Arrays](/en-us/windows/desktop/WinAuto/uiauto-workingwithsafearrays)

**Conceptual**

[Custom Properties, Events, and Control Patterns](/en-us/windows/desktop/WinAuto/uiauto-custompropertieseventscontrolpatterns)

[IUIAutomation](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomation)

[PollForPotentialSupportedProperties](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomation-pollforpotentialsupportedproperties)

**Reference**

---
