# CompareRuntimeIds

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomation-compareruntimeids)

# IUIAutomation::CompareRuntimeIds method (uiautomationclient.h)

Compares two integer arrays containing run-time identifiers (IDs) to determine whether their content is the same and they belong to the same UI element.

## Syntax

```
HRESULT CompareRuntimeIds(
  [in]          SAFEARRAY *runtimeId1,
  [in]          SAFEARRAY *runtimeId2,
  [out, retval] BOOL      *areSame
);
```

## Parameters

`[in] runtimeId1`

Type: **[SAFEARRAY](/en-us/windows/win32/api/oaidl/ns-oaidl-safearray)\***

The first ID to compare.

`[in] runtimeId2`

Type: **[SAFEARRAY](/en-us/windows/win32/api/oaidl/ns-oaidl-safearray)\***

The second ID to compare

`[out, retval] areSame`

Type: **[BOOL](/en-us/windows/desktop/WinProg/windows-data-types)\***

Receives **TRUE** if the IDs are the same, or **FALSE** otherwise.

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

[CompareElements](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomation-compareelements)

**Conceptual**

[GetRuntimeId](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-getruntimeid)

[IUIAutomation](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomation)

**Reference**

---
