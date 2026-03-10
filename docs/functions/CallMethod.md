# CallMethod

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nf-uiautomationcore-iuiautomationpatterninstance-callmethod)

# IUIAutomationPatternInstance::CallMethod method (uiautomationcore.h)

Client wrapper implements methods by calling this CallMethod function, specifying the parameters as an array of pointers.

## Syntax

```
HRESULT CallMethod(
  [in] UINT                        index,
  [in] const UIAutomationParameter *pParams,
  [in] UINT                        cParams
);
```

## Parameters

`[in] index`

Type: **[UINT](/en-us/windows/desktop/WinProg/windows-data-types)**

The index of the method.

`[in] pParams`

Type: **[UIAutomationParameter](/en-us/windows/desktop/api/uiautomationcore/ns-uiautomationcore-uiautomationparameter)\***

A pointer to an array of structures describing the parameters.

`[in] cParams`

Type: **[UINT](/en-us/windows/desktop/WinProg/windows-data-types)**

The count of parameters in *pParams*.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[IUIAutomationPatternInstance](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-iuiautomationpatterninstance)

---
