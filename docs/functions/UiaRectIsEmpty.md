# UiaRectIsEmpty

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/nf-uiautomationcoreapi-uiarectisempty)

# UiaRectIsEmpty function (uiautomationcoreapi.h)

**Note**  This function is deprecated. Client applications should use the Microsoft UI Automation Component Object Model (COM) interfaces instead.

Gets a Boolean value that specifies whether a rectangle has all its coordinates set to 0.

## Syntax

```
bool UiaRectIsEmpty(
  [in, ref] const UiaRect & rc
);
```

## Parameters

`[in, ref] rc`

Type: **const [UiaRect](/en-us/windows/desktop/api/uiautomationcore/ns-uiautomationcore-uiarect)**

A reference to a [UiaRect](/en-us/windows/desktop/api/uiautomationcore/ns-uiautomationcore-uiarect) structure that contains the coordinates of the rectangle.

## Return value

Type: **bool**

**TRUE** if the rectangle is empty; otherwise **FALSE**.

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
