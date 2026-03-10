# CreateAndConditionFromNativeArray

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomation-createandconditionfromnativearray)

# IUIAutomation::CreateAndConditionFromNativeArray method (uiautomationclient.h)

Creates a condition that selects elements from a native array, based on multiple conditions that must all be true.

## Syntax

```
HRESULT CreateAndConditionFromNativeArray(
  [in]          IUIAutomationCondition **conditions,
  [in]          int                    conditionCount,
  [out, retval] IUIAutomationCondition **newCondition
);
```

## Parameters

`[in] conditions`

Type: **[IUIAutomationCondition](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationcondition)\*\***

A pointer to an array of conditions to be combined.

`[in] conditionCount`

Type: **int**

The number of elements in the *conditions* array.

`[out, retval] newCondition`

Type: **[IUIAutomationCondition](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationcondition)\*\***

Receives a pointer to the combined condition.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

This method calls [AddRef](/en-us/windows/desktop/api/unknwn/nf-unknwn-iunknown-addref) on each pointer in the *conditions* array. This means you can call [Release](/en-us/windows/desktop/api/unknwn/nf-unknwn-iunknown-release) on those pointers after the call to **CreateAndConditionFromNativeArray** returns without invalidating the pointer returned from **CreateAndConditionFromNativeArray**. When you call **Release** on the pointer returned from **CreateAndConditionFromNativeArray**, UI Automation calls **Release** on each pointer in the *conditions* array.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[CreateAndCondition](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomation-createandcondition)

[CreateAndConditionFromArray](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomation-createandconditionfromarray)

[FindAll](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-findall)

[FindAllBuildCache](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-findallbuildcache)

[FindFirst](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-findfirst)

[FindFirstBuildCache](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-findfirstbuildcache)

[IUIAutomation](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomation)

[IUIAutomationCondition](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationcondition)

**Reference**

---
