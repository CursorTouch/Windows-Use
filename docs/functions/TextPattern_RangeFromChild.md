# TextPattern_RangeFromChild

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/nf-uiautomationcoreapi-textpattern_rangefromchild)

# TextPattern\_RangeFromChild function (uiautomationcoreapi.h)

**Note**  This function is deprecated. Client applications should use the Microsoft UI Automation Component Object Model (COM) interfaces instead.

Gets the text range that a given node spans.

## Syntax

```
HRESULT TextPattern_RangeFromChild(
  [in]  HUIAPATTERNOBJECT hobj,
  [in]  HUIANODE          hnodeChild,
  [out] HUIATEXTRANGE     *pRetVal
);
```

## Parameters

`[in] hobj`

Type: **HUIAPATTERNOBJECT**

A control pattern object.

`[in] hnodeChild`

Type: **HUIANODE**

Reference to a node that the client wants the text range for.

`[out] pRetVal`

Type: **HUIATEXTRANGE\***

When this function returns, contains the text range that the node spans.
This parameter is passed uninitialized.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

Returns S\_OK if successful or an error value otherwise.

## Remarks

As an example of how this function might be used,
a client can pass in an embedded hyperlink control and receive the range of text that it spans.

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
