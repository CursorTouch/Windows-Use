# PollForPotentialSupportedProperties

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomation-pollforpotentialsupportedproperties)

# IUIAutomation::PollForPotentialSupportedProperties method (uiautomationclient.h)

Retrieves the properties that might be supported on a UI Automation element.

## Syntax

```
HRESULT PollForPotentialSupportedProperties(
  [in]  IUIAutomationElement *pElement,
  [out] SAFEARRAY            **propertyIds,
  [out] SAFEARRAY            **propertyNames
);
```

## Parameters

`[in] pElement`

Type: **[IUIAutomationElement](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationelement)\***

The address of the UI Automation element to poll.

`[out] propertyIds`

Type: **SAFEARRAY(int)\*\***

Receives a pointer to an array of property identifiers. For a list of property IDs, see [Property Identifiers](/en-us/windows/desktop/WinAuto/uiauto-entry-propids).

`[out] propertyNames`

Type: **SAFEARRAY(BSTR)\*\***

Receives a pointer to an array of property names.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

This method is intended only for use by Microsoft UI Automation tools that need to scan for properties and control patterns. It is not intended to be used by UI Automation clients.

There is no guarantee that the element will support any particular property when asked for it later.

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

[PollForPotentialSupportedPatterns](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomation-pollforpotentialsupportedpatterns)

**Reference**

---
