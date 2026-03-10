# TransformPattern_Resize

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/nf-uiautomationcoreapi-transformpattern_resize)

# TransformPattern\_Resize function (uiautomationcoreapi.h)

**Note**  This function is deprecated. Client applications should use the Microsoft UI Automation Component Object Model (COM) interfaces instead.

Resizes an element on the screen.

## Syntax

```
HRESULT TransformPattern_Resize(
  [in] HUIAPATTERNOBJECT hobj,
  [in] double            width,
  [in] double            height
);
```

## Parameters

`[in] hobj`

Type: **HUIAPATTERNOBJECT**

The control pattern object.

`[in] width`

Type: **double**

The width, in pixels, to resize the element to.

`[in] height`

Type: **double**

The height, in pixels, to resize the element to.

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
