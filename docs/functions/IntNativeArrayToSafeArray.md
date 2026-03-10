# IntNativeArrayToSafeArray

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomation-intnativearraytosafearray)

# IUIAutomation::IntNativeArrayToSafeArray method (uiautomationclient.h)

Converts an array of integers to a [SAFEARRAY](/en-us/windows/win32/api/oaidl/ns-oaidl-safearray).

## Syntax

```
HRESULT IntNativeArrayToSafeArray(
  [in]          int       *array,
  [in]          int       arrayCount,
  [out, retval] SAFEARRAY **safeArray
);
```

## Parameters

`[in] array`

Type: **int\***

A pointer to an array of integers.

`[in] arrayCount`

Type: **int**

The number of elements in *array*.

`[out, retval] safeArray`

Type: **[SAFEARRAY](/en-us/windows/win32/api/oaidl/ns-oaidl-safearray)\*\***

Receives a pointer to the allocated SAFEARRAY.

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

[Best Practices for Using Safe Arrays](/en-us/windows/desktop/WinAuto/uiauto-workingwithsafearrays)

[IUIAutomation](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomation)

[IUIAutomation::IntSafeArrayToNativeArray](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomation-intsafearraytonativearray)

---
