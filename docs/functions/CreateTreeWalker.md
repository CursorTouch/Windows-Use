# CreateTreeWalker

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomation-createtreewalker)

# IUIAutomation::CreateTreeWalker method (uiautomationclient.h)

Retrieves a tree walker object that can be used to traverse the Microsoft UI Automation tree.

## Syntax

```
HRESULT CreateTreeWalker(
  [in]          IUIAutomationCondition  *pCondition,
  [out, retval] IUIAutomationTreeWalker **walker
);
```

## Parameters

`[in] pCondition`

Type: **[IUIAutomationCondition](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationcondition)\***

A pointer to a condition that specifies the elements of interest.

`[out, retval] walker`

Type: **[IUIAutomationTreeWalker](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationtreewalker)\*\***

Receives a pointer to the tree walker object.

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

---
