# GetChildrenAsNativeArray

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationorcondition-getchildrenasnativearray)

# IUIAutomationOrCondition::GetChildrenAsNativeArray method (uiautomationclient.h)

Retrieves the conditions that make up this "or" condition, as an ordinary array.

## Syntax

```
HRESULT GetChildrenAsNativeArray(
  [out] IUIAutomationCondition ***childArray,
  [out] int                    *childArrayCount
);
```

## Parameters

`[out] childArray`

Type: **[IUIAutomationCondition](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationcondition)\*\*\***

Receives a pointer to an array of [IUIAutomationCondition](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationcondition) interface pointers.

`[out] childArrayCount`

Type: **int\***

Receives the number of elements in the array.

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

[IUIAutomationOrCondition](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationorcondition)

[IUIAutomationOrCondition::GetChildren](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationorcondition-getchildren)

---
