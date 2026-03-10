# GetActiveComposition

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationtexteditpattern-getactivecomposition)

# IUIAutomationTextEditPattern::GetActiveComposition method (uiautomationclient.h)

Returns the active composition.

## Syntax

```
HRESULT GetActiveComposition(
  [out, retval] IUIAutomationTextRange **range
);
```

## Parameters

`[out, retval] range`

Type: **[IUIAutomationTextRange](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationtextrange)\*\***

Pointer to the range of the current conversion (none if there is no conversion).

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

Active composition is relevant to Input Method Editors (IMEs).

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 8.1 [desktop apps only] |
| **Minimum supported server** | Windows Server 2012 R2 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[IUIAutomationTextEditPattern](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationtexteditpattern)

[UI Automation Support for Textual Content](/en-us/windows/desktop/WinAuto/uiauto-ui-automation-textpattern-overview)

---
