# GetCurrentSelection

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationlegacyiaccessiblepattern-getcurrentselection)

# IUIAutomationLegacyIAccessiblePattern::GetCurrentSelection method (uiautomationclient.h)

Retrieves the Microsoft Active Accessibility property that identifies the selected children of this element.

## Syntax

```
HRESULT GetCurrentSelection(
  [out, retval] IUIAutomationElementArray **pvarSelectedChildren
);
```

## Parameters

`[out, retval] pvarSelectedChildren`

Type: **[IUIAutomationElementArray](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationelementarray)\*\***

Receives a pointer to the collection of the selected child elements.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7 [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[IUIAutomationLegacyIAccessiblePattern](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationlegacyiaccessiblepattern)

---
