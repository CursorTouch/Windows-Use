# RangeFromAnnotation

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationtextpattern2-rangefromannotation)

# IUIAutomationTextPattern2::RangeFromAnnotation method (uiautomationclient.h)

Retrieves a text range containing the text that is the target of the annotation associated with the specified annotation element.

## Syntax

```
HRESULT RangeFromAnnotation(
  [in]          IUIAutomationElement   *annotation,
  [out, retval] IUIAutomationTextRange **range
);
```

## Parameters

`[in] annotation`

Type: **[IUIAutomationElement](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationelement)\***

The annotation element for which to retrieve the target text. This element is a sibling of the element that implements [IUIAutomationTextPattern2](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationtextpattern2) for the document.

`[out, retval] range`

Type: **[IUIAutomationTextRange](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationtextrange)\*\***

Receives a text range that contains the target text of the annotation.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 8 [desktop apps only] |
| **Minimum supported server** | Windows Server 2012 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[IUIAutomationTextPattern2](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationtextpattern2)

[UI Automation Support for Textual Content](/en-us/windows/desktop/WinAuto/uiauto-ui-automation-textpattern-overview)

[Working with Text-based Controls](/en-us/windows/desktop/WinAuto/uiauto-workingwithtextbasedcontrols)

---
