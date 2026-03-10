# TextRange_CompareEndpoints

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/nf-uiautomationcoreapi-textrange_compareendpoints)

# TextRange\_CompareEndpoints function (uiautomationcoreapi.h)

**Note**  This function is deprecated. Client applications should use the Microsoft UI Automation Component Object Model (COM) interfaces instead.

Returns a value indicating whether two text ranges have identical endpoints.

## Syntax

```
HRESULT TextRange_CompareEndpoints(
  [in]  HUIATEXTRANGE            hobj,
  [in]  TextPatternRangeEndpoint endpoint,
  [in]  HUIATEXTRANGE            targetRange,
  [in]  TextPatternRangeEndpoint targetEndpoint,
  [out] int                      *pRetVal
);
```

## Parameters

`[in] hobj`

Type: **HUIATEXTRANGE**

A text range object.

`[in] endpoint`

Type: **TextPatternRangeEndpoint**

The starting or ending endpoint of *hobj*.

`[in] targetRange`

Type: **ITextRangeInteropProvider\***

The text range that is being compared against.

`[in] targetEndpoint`

Type: **TextPatternRangeEndpoint**

The starting or ending endpoint of *targetRange*.

`[out] pRetVal`

Type: **int\***

The address of a variable that receives a pointer to a value that indicates whether two text ranges have identical endpoints.
This parameter is passed uninitialized.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

Returns S\_OK if successful or an error value otherwise.

## Remarks

The returned value is <0 if the caller's endpoint occurs earlier in the text than the target endpoint;
0 if the caller's endpoint is at the same location as the target endpoint; and
>0 if the caller's endpoint occurs later in the text than the target endpoint.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps only] |
| **Minimum supported server** | Windows Server 2003 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationcoreapi.h |
| **Library** | Uiautomationcore.lib |
| **DLL** | Uiautomationcore.dll |

---
