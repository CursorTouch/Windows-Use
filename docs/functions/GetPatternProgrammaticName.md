# GetPatternProgrammaticName

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomation-getpatternprogrammaticname)

# IUIAutomation::GetPatternProgrammaticName method (uiautomationclient.h)

Retrieves the registered programmatic name of a control pattern.

## Syntax

```
HRESULT GetPatternProgrammaticName(
  [in]          PATTERNID pattern,
  [out, retval] BSTR      *name
);
```

## Parameters

`[in] pattern`

Type: **PATTERNID**

The identifier of the control pattern. For a list of control pattern IDs, see [Control Pattern Identifiers](/en-us/windows/desktop/WinAuto/uiauto-controlpattern-ids).

`[out, retval] name`

Type: **BSTR\***

Receives the registered programmatic name.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

The programmatic name is intended for debugging and diagnostic purposes only. The string is not localized.

This property should not be used in string comparisons. To determine whether two control patterns are the same, compare the control pattern identifiers directly.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps only] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

---
