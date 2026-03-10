# UiaRectSetEmpty

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/nf-uiautomationcoreapi-uiarectsetempty)

# UiaRectSetEmpty function (uiautomationcoreapi.h)

**Note**  This function is deprecated. Client applications should use the Microsoft UI Automation Component Object Model (COM) interfaces instead.

Sets the elements of a [UiaRect](/en-us/windows/desktop/api/uiautomationcore/ns-uiautomationcore-uiarect) structure to 0.

## Syntax

```
void UiaRectSetEmpty(
  [in, ref] UiaRect & rc
);
```

## Parameters

`[in, ref] rc`

Type: **[UiaRect](/en-us/windows/desktop/api/uiautomationcore/ns-uiautomationcore-uiarect)**

A reference to a [UiaRect](/en-us/windows/desktop/api/uiautomationcore/ns-uiautomationcore-uiarect) structure.

## Return value

None

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
