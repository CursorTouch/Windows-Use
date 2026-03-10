# GetRootElement

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomation-getrootelement)

# IUIAutomation::GetRootElement method (uiautomationclient.h)

Retrieves the UI Automation element that represents the desktop.

## Syntax

```
HRESULT GetRootElement(
  [out, retval] IUIAutomationElement **root
);
```

## Parameters

`[out, retval] root`

Type: **[IUIAutomationElement](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationelement)\*\***

Receives a pointer to the UI Automation element.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

You can use the root element as a starting point for finding other elements, using the [FindAll](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-findall) and [FindFirst](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-findfirst) methods.

When searching from the root element, be sure to specify [TreeScope\_Children](/en-us/windows/desktop/api/uiautomationclient/ne-uiautomationclient-treescope) in the scope of the search, not [TreeScope\_Descendants](/en-us/windows/desktop/api/uiautomationclient/ne-uiautomationclient-treescope). A search through the entire subtree of the desktop could iterate through thousands of items and lead to a stack overflow.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[IUIAutomation](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomation)

[IUIAutomation::GetRootElementBuildCache](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomation-getrootelementbuildcache)

---
