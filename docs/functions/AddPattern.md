# AddPattern

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationcacherequest-addpattern)

# IUIAutomationCacheRequest::AddPattern method (uiautomationclient.h)

Adds a control pattern to the cache request.

## Syntax

```
HRESULT AddPattern(
  [in] PATTERNID patternId
);
```

## Parameters

`[in] patternId`

Type: **PATTERNID**

The identifier of the control pattern to add to the cache request. For a list of control pattern IDs, see [Control Pattern Identifiers](/en-us/windows/desktop/WinAuto/uiauto-controlpattern-ids).

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

Adding a control pattern that is already in the cache request has no effect.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[IUIAutomationCacheRequest](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationcacherequest)

---
