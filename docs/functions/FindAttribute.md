# FindAttribute

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationtextrange-findattribute)

# IUIAutomationTextRange::FindAttribute method (uiautomationclient.h)

Retrieves a text range subset that has the specified text attribute value.

## Syntax

```
HRESULT FindAttribute(
  [in]          TEXTATTRIBUTEID        attr,
  [in]          VARIANT                val,
  [in]          BOOL                   backward,
  [out, retval] IUIAutomationTextRange **found
);
```

## Parameters

`[in] attr`

Type: **TEXTATTRIBUTEID**

The identifier of the text attribute for the text range subset being retrieved. For a list of text attribute IDs, see [Text Attribute Identifiers](/en-us/windows/desktop/WinAuto/uiauto-textattribute-ids).

`[in] val`

Type: **[VARIANT](/en-us/windows/desktop/api/oaidl/ns-oaidl-variant)**

The value of the attribute. This value must match the type specified for the attribute.

`[in] backward`

Type: **[BOOL](/en-us/windows/desktop/WinProg/windows-data-types)**

**TRUE** if the last occurring text range should be returned instead of the first; otherwise **FALSE**.

`[out, retval] found`

Type: **[IUIAutomationTextRange](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationtextrange)\*\***

Receives a pointer to the text range having a matching attribute and attribute value; otherwise **NULL**.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

The **FindAttribute** method retrieves matching text regardless of whether the text is hidden or visible. Use [UIA\_IsHiddenAttributeId](/en-us/windows/desktop/WinAuto/uiauto-textattribute-ids) to check text visibility.

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
