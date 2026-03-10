# TextRange_MoveEndpointByRange

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/nf-uiautomationcoreapi-textrange_moveendpointbyrange)

# TextRange\_MoveEndpointByRange function (uiautomationcoreapi.h)

**Note**  This function is deprecated. Client applications should use the Microsoft UI Automation Component Object Model (COM) interfaces instead.

Moves an endpoint of one range to the endpoint of another range.

## Syntax

```
HRESULT TextRange_MoveEndpointByRange(
  [in] HUIATEXTRANGE            hobj,
  [in] TextPatternRangeEndpoint endpoint,
  [in] HUIATEXTRANGE            targetRange,
  [in] TextPatternRangeEndpoint targetEndpoint
);
```

## Parameters

`[in] hobj`

Type: **HUIATEXTRANGE**

The text range object whose endpoint is to move.

`[in] endpoint`

Type: **TextPatternRangeEndpoint**

The endpoint to move (either the start or the end).

`[in] targetRange`

Type: **HUIATEXTRANGE**

The text range that contains the target endpoint.

`[in] targetEndpoint`

Type: **TextPatternRangeEndpoint**

The target endpoint to move to (either the start or the end).

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

Returns S\_OK if successful or an error value otherwise.

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
