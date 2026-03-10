# CreateAndCondition

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomation-createandcondition)

# IUIAutomation::CreateAndCondition method (uiautomationclient.h)

Creates a condition that selects elements that match both of two conditions.

## Syntax

```
HRESULT CreateAndCondition(
  [in]          IUIAutomationCondition *condition1,
  [in]          IUIAutomationCondition *condition2,
  [out, retval] IUIAutomationCondition **newCondition
);
```

## Parameters

`[in] condition1`

Type: **[IUIAutomationCondition](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationcondition)\***

A pointer to the first condition to match.

`[in] condition2`

Type: **[IUIAutomationCondition](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationcondition)\***

A pointer to the second condition to match.

`[out, retval] newCondition`

Type: **[IUIAutomationCondition](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationcondition)\*\***

Receives a pointer to the combined condition.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

A condition that combines more than two simple conditions can be created by using [IUIAutomation::CreateAndConditionFromArray](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomation-createandconditionfromarray) or [IUIAutomation::CreateAndConditionFromNativeArray](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomation-createandconditionfromnativearray).

The **CreateAndCondition** method calls [AddRef](/en-us/windows/desktop/api/unknwn/nf-unknwn-iunknown-addref) on the *condition1* and *condition2* pointers. This means you can call [Release](/en-us/windows/desktop/api/unknwn/nf-unknwn-iunknown-release) on those two pointers after the call to **CreateAndCondition** returns without invalidating the pointer returned from **CreateAndCondition**. When you call **Release** on the pointer returned from **CreateAndCondition**, UI Automation calls **Release** on the *condition1* and *condition2* pointers.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[CreateAndConditionFromArray](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomation-createandconditionfromarray)

[FindAll](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-findall)

[FindAllBuildCache](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-findallbuildcache)

[FindFirst](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-findfirst)

[FindFirstBuildCache](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-findfirstbuildcache)

[IUIAutomation](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomation)

[IUIAutomationCondition](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationcondition)

**Reference**

---
