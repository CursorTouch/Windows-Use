# GetFocus

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nf-uiautomationcore-irawelementproviderfragmentroot-getfocus)

# IRawElementProviderFragmentRoot::GetFocus method (uiautomationcore.h)

Retrieves the element in this fragment that has the input focus.

## Syntax

```
HRESULT GetFocus(
  [out, retval] IRawElementProviderFragment **pRetVal
);
```

## Parameters

`[out, retval] pRetVal`

Type: **[IRawElementProviderFragment](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-irawelementproviderfragment)\*\***

Receives a pointer to the [IRawElementProviderFragment](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-irawelementproviderfragment)
interface of the
element in this fragment that has the input focus, if any; otherwise **NULL**.
This parameter is passed uninitialized.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2003 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[IRawElementProviderFragmentRoot](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-irawelementproviderfragmentroot)

---
