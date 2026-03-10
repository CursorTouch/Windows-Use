# IntSafeArrayToNativeArray

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomation-intsafearraytonativearray)

# IUIAutomation::IntSafeArrayToNativeArray method (uiautomationclient.h)

Converts a [SAFEARRAY](/en-us/windows/win32/api/oaidl/ns-oaidl-safearray) of integers to an array.

## Syntax

```
HRESULT IntSafeArrayToNativeArray(
  [in]          SAFEARRAY *intArray,
  [out]         int       **array,
  [out, retval] int       *arrayCount
);
```

## Parameters

`[in] intArray`

Type: **[SAFEARRAY](/en-us/windows/win32/api/oaidl/ns-oaidl-safearray)\***

A pointer to the SAFEARRAY to convert.

`[out] array`

Type: **int\*\***

Receives a pointer to the allocated array.

`[out, retval] arrayCount`

Type: **int\***

Receives the number of elements in *array*.

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

[IntNativeArrayToSafeArray](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomation-intnativearraytosafearray)

---
