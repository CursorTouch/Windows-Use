# CheckNotSupported

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomation-checknotsupported)

# IUIAutomation::CheckNotSupported method (uiautomationclient.h)

Checks a provided [VARIANT](/en-us/windows/desktop/api/oaidl/ns-oaidl-variant) to see if it contains the Not Supported identifier.

## Syntax

```
HRESULT CheckNotSupported(
  [in]  VARIANT value,
  [out] BOOL    *isNotSupported
);
```

## Parameters

`[in] value`

Type: **[VARIANT](/en-us/windows/desktop/api/oaidl/ns-oaidl-variant)**

The value to check.

`[out] isNotSupported`

Type: **[BOOL](/en-us/windows/desktop/WinProg/windows-data-types)\***

Receives **TRUE** if the provided [VARIANT](/en-us/windows/desktop/api/oaidl/ns-oaidl-variant) contains the Not Supported identifier, or **FALSE** otherwise.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

After retrieving a property for a UI Automation element, call this method to determine whether the element supports the retrieved property. **CheckNotSupported** is typically called after calling a property retrieving method such as [GetCurrentPropertyValue](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-getcurrentpropertyvalue).

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[IUIAutomation](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomation)

[IUIAutomation::ReservedNotSupportedValue](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomation-get_reservednotsupportedvalue)

---
