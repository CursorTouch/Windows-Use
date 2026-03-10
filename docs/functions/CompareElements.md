# CompareElements

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomation-compareelements)

# IUIAutomation::CompareElements method (uiautomationclient.h)

Compares two UI Automation elements to determine whether they represent the same underlying UI element.

## Syntax

```
HRESULT CompareElements(
  [in]          IUIAutomationElement *el1,
  [in]          IUIAutomationElement *el2,
  [out, retval] BOOL                 *areSame
);
```

## Parameters

`[in] el1`

Type: **[IUIAutomationElement](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationelement)\***

A pointer to the first element to compare.

`[in] el2`

Type: **[IUIAutomationElement](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationelement)\***

A pointer to the second element to compare.

`[out, retval] areSame`

Type: **[BOOL](/en-us/windows/desktop/WinProg/windows-data-types)\***

Receives **TRUE** if the run-time identifiers of the elements are the same, or **FALSE** otherwise.

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

[IUIAutomation](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomation)

[IUIAutomation::CompareRuntimeIds](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomation-compareruntimeids)

---
