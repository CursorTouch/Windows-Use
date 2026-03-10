# Select

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationlegacyiaccessiblepattern-select)

# IUIAutomationLegacyIAccessiblePattern::Select method (uiautomationclient.h)

Performs a Microsoft Active Accessibility selection.

## Syntax

```
HRESULT Select(
  long flagsSelect
);
```

## Parameters

`flagsSelect`

Type: **long**

Specifies which selection or focus operations are to be performed. This parameter must have a combination of the values described in [SELFLAG Constants](/en-us/windows/desktop/WinAuto/selflag).

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
