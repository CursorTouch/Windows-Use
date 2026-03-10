# get_CurrentHelpText

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-get_currenthelptext)

# IUIAutomationElement::get\_CurrentHelpText method (uiautomationclient.h)

Retrieves the help text for the element.

This property is read-only.

## Syntax

```
HRESULT get_CurrentHelpText(
  BSTR *retVal
);
```

## Parameters

`retVal`

## Return value

None

## Remarks

This information is typically obtained from tooltips.

**Caution**  Do not retrieve the [CachedHelpText](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-get_cachedhelptext) property from a control that is based on the SysListview32 class. Doing so could cause the system to become unstable and data to be lost. A client application can discover whether a control is based on SysListview32 by retrieving the [CachedClassName](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-get_cachedclassname) or [CurrentClassName](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-get_currentclassname) property from the control.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[Automation Element Property IDs](/en-us/windows/desktop/WinAuto/uiauto-automation-element-propids)

[CachedHelpText](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-get_cachedhelptext)

[IUIAutomationElement](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationelement)

**Reference**

---
