# CreateOrConditionFromArray

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomation-createorconditionfromarray)

# IUIAutomation::CreateOrConditionFromArray method (uiautomationclient.h)

Creates a combination of two or more conditions where a match exists if any of the conditions is true.

## Syntax

```
HRESULT CreateOrConditionFromArray(
  [in]          SAFEARRAY              *conditions,
  [out, retval] IUIAutomationCondition **newCondition
);
```

## Parameters

`[in] conditions`

Type: **[SAFEARRAY](/en-us/windows/win32/api/oaidl/ns-oaidl-safearray)\***

A pointer to the conditions.

`[out, retval] newCondition`

Type: **[IUIAutomationCondition](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationcondition)\*\***

Receives a pointer to the combined condition.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

This method calls [AddRef](/en-us/windows/desktop/api/unknwn/nf-unknwn-iunknown-addref) on each pointer in the *conditions* array. This means you can call [Release](/en-us/windows/desktop/api/unknwn/nf-unknwn-iunknown-release) on those pointers after the call to **CreateOrConditionFromArray** returns without invalidating the pointer returned from **CreateOrConditionFromArray**. When you call **Release** on the pointer returned from **CreateOrConditionFromArray**, UI Automation calls **Release** on each pointer in the *conditions* array.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[Best Practices for Using Safe Arrays](/en-us/windows/desktop/WinAuto/uiauto-workingwithsafearrays)

**Conceptual**

[CreateOrCondition](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomation-createorcondition)

[CreateOrConditionFromNativeArray](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomation-createorconditionfromnativearray)

[FindAll](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-findall)

[FindAllBuildCache](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-findallbuildcache)

[FindFirst](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-findfirst)

[FindFirstBuildCache](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-findfirstbuildcache)

[IUIAutomation](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomation)

[IUIAutomationCondition](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationcondition)

**Reference**

---
