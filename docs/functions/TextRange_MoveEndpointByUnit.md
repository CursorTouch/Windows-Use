# TextRange_MoveEndpointByUnit

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/nf-uiautomationcoreapi-textrange_moveendpointbyunit)

# TextRange\_MoveEndpointByUnit function (uiautomationcoreapi.h)

**Note**  This function is deprecated. Client applications should use the Microsoft UI Automation Component Object Model (COM) interfaces instead.

Moves an endpoint of the range the specified number of units.

## Syntax

```
HRESULT TextRange_MoveEndpointByUnit(
  [in]  HUIATEXTRANGE            hobj,
  [in]  TextPatternRangeEndpoint endpoint,
  [in]  TextUnit                 unit,
  [in]  int                      count,
  [out] int                      *pRetVal
);
```

## Parameters

`[in] hobj`

Type: **HUIATEXTRANGE**

A text range object.

`[in] endpoint`

Type: **TextPatternRangeEndpoint**

The endpoint to move (either the start or the end).

`[in] unit`

Type: **[TextUnit](/en-us/windows/desktop/api/uiautomationcore/ne-uiautomationcore-textunit)**

The unit, such as Page, Line, or Word.

`[in] count`

Type: **int**

The number of units to move. A positive value moves the range forward; a negative value
moves it backward.

`[out] pRetVal`

Type: **int\***

When this function returns, contains
the number of units the endpoint actually moved.
This parameter is passed uninitialized.

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
