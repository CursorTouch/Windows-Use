# GetAttributeValues

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationtextrange3-getattributevalues)

# IUIAutomationTextRange3::GetAttributeValues method (uiautomationclient.h)

Returns all of the requested text attribute values for a text range in a single cross-process call. This is equivalent to calling [GetAttributeValue](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationtextrange-getattributevalue), except it can retrieve multiple values instead of just one.

## Syntax

```
HRESULT GetAttributeValues(
  [in]          const TEXTATTRIBUTEID *attributeIds,
  [in]          int                   attributeIdCount,
  [out, retval] SAFEARRAY             **attributeValues
);
```

## Parameters

`[in] attributeIds`

A list of [text attribute identifiers](/en-us/windows/desktop/WinAuto/uiauto-textattribute-ids).

`[in] attributeIdCount`

The number of [text attribute identifiers](/en-us/windows/desktop/WinAuto/uiauto-textattribute-ids) in the *attributeIds* list.

`[out, retval] attributeValues`

A **SAFEARRAY** of **VARIANT** containing values to corresponding text attributes for a text range.

## Return value

Returns **S\_OK** if successful, otherwise an **HRESULT** error code.

## Remarks

**GetAttributeValues** only gets the text attributes that are supplied in the call.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 10, version 1703 [desktop apps only] |
| **Minimum supported server** | Windows Server 2016 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[IUIAutomationTextRange3](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationtextrange3)

[UI Automation Support for Textual Content](/en-us/windows/desktop/WinAuto/uiauto-ui-automation-textpattern-overview)

---
