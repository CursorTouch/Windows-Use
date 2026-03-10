# GetUnderlyingObjectModel

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationobjectmodelpattern-getunderlyingobjectmodel)

# IUIAutomationObjectModelPattern::GetUnderlyingObjectModel method (uiautomationclient.h)

Retrieves an interface used to access the underlying object model of the provider.

## Syntax

```
HRESULT GetUnderlyingObjectModel(
  [out, retval] IUnknown **retVal
);
```

## Parameters

`[out, retval] retVal`

Type: **[IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown)\*\***

Receives an interface for accessing the underlying object model.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

Client applications can use the object model to directly access the content of the control or application.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 8 [desktop apps only] |
| **Minimum supported server** | Windows Server 2012 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[IUIAutomationObjectModelPattern](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationobjectmodelpattern)

---
