# SynchronizedInputPattern_StartListening

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/nf-uiautomationcoreapi-synchronizedinputpattern_startlistening)

# SynchronizedInputPattern\_StartListening function (uiautomationcoreapi.h)

**Note**  This function is deprecated. Client applications should use the Microsoft UI Automation Component Object Model (COM) interfaces instead.

Causes the UI Automation provider to start listening for mouse or keyboard input.

## Syntax

```
HRESULT SynchronizedInputPattern_StartListening(
  [in] HUIAPATTERNOBJECT     hobj,
  [in] SynchronizedInputType inputType
);
```

## Parameters

`[in] hobj`

Type: **HUIAPATTERNOBJECT**

The *control pattern* object.

`[in] inputType`

Type: **[SynchronizedInputType](/en-us/windows/desktop/api/uiautomationcore/ne-uiautomationcore-synchronizedinputtype)**

A combination of values from the [SynchronizedInputType](/en-us/windows/desktop/api/uiautomationcore/ne-uiautomationcore-synchronizedinputtype) enumerated type specifying the type of input for which to listen.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

Returns S\_OK if successful or an error value otherwise.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationcoreapi.h |
| **Library** | Uiautomationcore.lib |
| **DLL** | Uiautomationcore.dll |

---
