# SafeArrayToRectNativeArray

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomation-safearraytorectnativearray)

# IUIAutomation::SafeArrayToRectNativeArray method (uiautomationclient.h)

Converts a [SAFEARRAY](/en-us/windows/win32/api/oaidl/ns-oaidl-safearray) containing rectangle coordinates to an array of type [RECT](/en-us/windows/desktop/api/windef/ns-windef-rect).

## Syntax

```
HRESULT SafeArrayToRectNativeArray(
  [in]          SAFEARRAY *rects,
  [out]         RECT      **rectArray,
  [out, retval] int       *rectArrayCount
);
```

## Parameters

`[in] rects`

Type: **[SAFEARRAY](/en-us/windows/win32/api/oaidl/ns-oaidl-safearray)\***

A pointer to an array containing rectangle coordinates.

`[out] rectArray`

Type: **[RECT](/en-us/windows/desktop/api/windef/ns-windef-rect)\*\***

Receives a pointer to an array of structures containing rectangle coordinates.

`[out, retval] rectArrayCount`

Type: **int\***

Receives the number of elements in *rectArray*.

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
