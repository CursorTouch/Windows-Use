# get_CachedAccessKey

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-get_cachedaccesskey)

# IUIAutomationElement::get\_CachedAccessKey method (uiautomationclient.h)

Retrieves the cached access key character for the element.

This property is read-only.

## Syntax

```
HRESULT get_CachedAccessKey(
  BSTR *retVal
);
```

## Parameters

`retVal`

## Return value

None

## Remarks

An access key is a character in the text of a menu, menu item, or label of a control such as a button that activates the attached menu function. For example, the letter "O" is often used to invoke the Open file common dialog box from a File menu. Microsoft UI Automation elements that have the access key property set always implement the [Invoke](/en-us/windows/desktop/WinAuto/uiauto-implementinginvoke) control pattern.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7 [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[Automation Element Property IDs](/en-us/windows/desktop/WinAuto/uiauto-automation-element-propids)

[CurrentAccessKey](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-get_currentaccesskey)

[IUIAutomationElement](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationelement)

**Reference**

---
