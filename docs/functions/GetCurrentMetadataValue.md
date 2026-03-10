# GetCurrentMetadataValue

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement7-getcurrentmetadatavalue)

# IUIAutomationElement7::GetCurrentMetadataValue method (uiautomationclient.h)

Gets metadata from the UI Automation element that indicates how the information should be interpreted. For example, should the string "1/4" be interpreted as a fraction or a date?

## Syntax

```
HRESULT GetCurrentMetadataValue(
  [in]          int        targetId,
  [in]          METADATAID metadataId,
  [out, retval] VARIANT    *returnVal
);
```

## Parameters

`[in] targetId`

The ID of the property to retrieve.

`[in] metadataId`

Specifies the type of metadata to retrieve.

`[out, retval] returnVal`

The metadata.

## Return value

Returns **S\_OK** if successful, otherwise an **HRESULT** error code.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 10, version 1703 [desktop apps only] |
| **Minimum supported server** | Windows Server 2016 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |
| **DLL** | UIAutomationCore.dll |

## See also

[IUIAutomationElement7](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationelement7)

[SayAsInterpretAs](/en-us/windows/desktop/api/uiautomationcore/ne-uiautomationcore-sayasinterpretas)

---
