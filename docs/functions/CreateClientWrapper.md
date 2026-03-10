# CreateClientWrapper

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nf-uiautomationcore-iuiautomationpatternhandler-createclientwrapper)

# IUIAutomationPatternHandler::CreateClientWrapper method (uiautomationcore.h)

Creates an object that enables a client application to interact with a custom *control pattern*.

## Syntax

```
HRESULT CreateClientWrapper(
  [in]          IUIAutomationPatternInstance *pPatternInstance,
  [out, retval] IUnknown                     **pClientWrapper
);
```

## Parameters

`[in] pPatternInstance`

Type: **[IUIAutomationPatternInstance](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-iuiautomationpatterninstance)\***

A pointer to the instance of the control pattern that will be used by the wrapper.

`[out, retval] pClientWrapper`

Type: **[IUnknown](/en-us/windows/desktop/api/unknwn/nn-unknwn-iunknown)\*\***

Receives a pointer to the wrapper object.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

The wrapper object exposes methods and properties of the *control pattern*. The implementation of the wrapper class passes these calls to Microsoft UI Automation by calling [CallMethod](/en-us/windows/desktop/api/uiautomationcore/nf-uiautomationcore-iuiautomationpatterninstance-callmethod) and [GetProperty](/en-us/windows/desktop/api/uiautomationcore/nf-uiautomationcore-iuiautomationpatterninstance-getproperty).

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[IUIAutomationPatternHandler](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-iuiautomationpatternhandler)

---
