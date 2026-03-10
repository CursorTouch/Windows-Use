# GetAttributeValue

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationtextrange-getattributevalue)

# IUIAutomationTextRange::GetAttributeValue method (uiautomationclient.h)

Retrieves the value of the specified text attribute across the entire text range.

## Syntax

```
HRESULT GetAttributeValue(
  [in]          TEXTATTRIBUTEID attr,
  [out, retval] VARIANT         *value
);
```

## Parameters

`[in] attr`

Type: **TEXTATTRIBUTEID**

The identifier of the text attribute. For a list of text attribute IDs, see [Text Attribute Identifiers](/en-us/windows/desktop/WinAuto/uiauto-textattribute-ids).

`[out, retval] value`

Type: **[VARIANT](/en-us/windows/desktop/api/oaidl/ns-oaidl-variant)\***

Receives the value of the specified attribute.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

The type of value retrieved by this method depends on the *attr* parameter.
For example, calling **GetAttributeValue** with the *attr* parameter set to [UIA\_FontNameAttributeId](/en-us/windows/desktop/WinAuto/uiauto-textattribute-ids) returns a string that represents the font name of the text range, while calling **GetAttributeValue** with *attr* set to [UIA\_IsItalicAttributeId](/en-us/windows/desktop/WinAuto/uiauto-textattribute-ids) would return a boolean.

If the attribute specified by *attr* is not supported, the *value* parameter receives a value that is equivalent to the [IUIAutomation::ReservedNotSupportedValue](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomation-get_reservednotsupportedvalue) property.

A text range can include more than one value for a particular attribute. For example, if a text range includes more than one font, the FontName attribute will have multiple values. An attribute with more than one value is called a *mixed attribute*. You can determine if a particular attribute is a mixed attribute by comparing the value retrieved from **GetAttributeValue** with the [UIAutomation::ReservedMixedAttributeValue](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomation-get_reservedmixedattributevalue) property.

The **GetAttributeValue** method retrieves the attribute value regardless of whether the text is hidden or visible.
Use UIA\_ IsHiddenAttributeId to check text visibility.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[IUIAutomationTextRange](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationtextrange)

[UI Automation Support for Textual Content](/en-us/windows/desktop/WinAuto/uiauto-ui-automation-textpattern-overview)

---
