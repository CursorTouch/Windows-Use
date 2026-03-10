# GetEmbeddedFragmentRoots

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nf-uiautomationcore-irawelementproviderfragment-getembeddedfragmentroots)

# IRawElementProviderFragment::GetEmbeddedFragmentRoots method (uiautomationcore.h)

Retrieves an array of root fragments that are embedded in the Microsoft UI Automation tree rooted at the current element.

## Syntax

```
HRESULT GetEmbeddedFragmentRoots(
  [out, retval] SAFEARRAY **pRetVal
);
```

## Parameters

`[out, retval] pRetVal`

Type: **SAFEARRAY\*\***

Receives an array of pointers to the root fragments, or **NULL** (see Remarks). This parameter is passed uninitialized.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

This method returns an array of fragments only if the current element is hosting another automation framework.
Most providers return **NULL**.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2003 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[Best Practices for Using Safe Arrays](/en-us/windows/desktop/WinAuto/uiauto-workingwithsafearrays)

**Conceptual**

[IRawElementProviderFragment](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-irawelementproviderfragment)

**Reference**

---
