# get_CachedControlType

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-get_cachedcontroltype)

# IUIAutomationElement::get\_CachedControlType method (uiautomationclient.h)

Retrieves a cached value that indicates the control type of the element.

This property is read-only.

## Syntax

```
HRESULT get_CachedControlType(
  CONTROLTYPEID *retVal
);
```

## Parameters

`retVal`

## Return value

None

## Remarks

Control types describe a known interaction model for UI Automation elements without relying on a localized control type or combination of complex logic rules. This property cannot change at run time unless the control supports the [IUIAutomationMultipleViewPattern](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationmultipleviewpattern) interface. An example is the Win32 ListView control, which can change from a data grid to a list, depending on the current view.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[Automation Element Property IDs](/en-us/windows/desktop/WinAuto/uiauto-automation-element-propids)

[CurrentControlType](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-get_currentcontroltype)

[IUIAutomationElement](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationelement)

**Reference**

---
