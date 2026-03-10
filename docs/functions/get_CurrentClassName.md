# get_CurrentClassName

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-get_currentclassname)

# IUIAutomationElement::get\_CurrentClassName method (uiautomationclient.h)

Retrieves the class name of the element.

This property is read-only.

## Syntax

```
HRESULT get_CurrentClassName(
  BSTR *retVal
);
```

## Parameters

`retVal`

## Return value

None

## Remarks

The value of this property is implementation-defined. The property is useful in testing environments.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[Automation Element Property IDs](/en-us/windows/desktop/WinAuto/uiauto-automation-element-propids)

[CachedClassName](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-get_cachedclassname)

[IUIAutomationElement](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationelement)

**Reference**

---
