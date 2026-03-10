# GetElement

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationtextrangearray-getelement)

# IUIAutomationTextRangeArray::GetElement method (uiautomationclient.h)

Retrieves a text range from the collection.

## Syntax

```
HRESULT GetElement(
  [in]          int                    index,
  [out, retval] IUIAutomationTextRange **element
);
```

## Parameters

`[in] index`

Type: **int**

The zero-based index of the item.

`[out, retval] element`

Type: **[IUIAutomationTextRange](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationtextrange)\*\***

Receives a pointer to the text range.

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

[IUIAutomationTextRangeArray](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationtextrangearray)

[UI Automation Support for Textual Content](/en-us/windows/desktop/WinAuto/uiauto-ui-automation-textpattern-overview)

---
