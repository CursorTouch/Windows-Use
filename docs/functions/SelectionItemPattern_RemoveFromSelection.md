# SelectionItemPattern_RemoveFromSelection

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/nf-uiautomationcoreapi-selectionitempattern_removefromselection)

# SelectionItemPattern\_RemoveFromSelection function (uiautomationcoreapi.h)

**Note**  This function is deprecated. Client applications should use the Microsoft UI Automation Component Object Model (COM) interfaces instead.

Removes an element from the selection in a selection container.

## Syntax

```
HRESULT SelectionItemPattern_RemoveFromSelection(
  [in] HUIAPATTERNOBJECT hobj
);
```

## Parameters

`[in] hobj`

Type: **HUIAPATTERNOBJECT**

The control pattern object.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

Returns S\_OK if successful or an error value otherwise.

## Remarks

The function has no effect if an attempt is made to remove the last selected element in a control that requires at
least one element to be selected.

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
