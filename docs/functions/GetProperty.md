# GetProperty

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nf-uiautomationcore-iuiautomationpatterninstance-getproperty)

# IUIAutomationPatternInstance::GetProperty method (uiautomationcore.h)

The client wrapper object implements the **IUIAutomation::get\_Current***X* and **IUIAutomationElement::get\_Cached***X* methods by calling this function, specifying the property by index.

## Syntax

```
HRESULT GetProperty(
  [in]          UINT             index,
  [in]          BOOL             cached,
  [in]          UIAutomationType type,
  [out, retval] void             *pPtr
);
```

## Parameters

`[in] index`

Type: **[UINT](/en-us/windows/desktop/WinProg/windows-data-types)**

The index of the property.

`[in] cached`

Type: **[BOOL](/en-us/windows/desktop/WinProg/windows-data-types)**

**TRUE** if the property should be retrieved from the cache, otherwise **FALSE**.

`[in] type`

Type: **[UIAutomationType](/en-us/windows/desktop/api/uiautomationcore/ne-uiautomationcore-uiautomationtype)**

A value indicating the data type of the property.

`[out, retval] pPtr`

Type: **void\***

Receives the value of the property.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[IUIAutomationPatternInstance](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-iuiautomationpatterninstance)

---
