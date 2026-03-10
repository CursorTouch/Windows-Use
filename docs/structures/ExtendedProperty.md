# ExtendedProperty

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/ns-uiautomationclient-extendedproperty)

# ExtendedProperty structure (uiautomationclient.h)

Contains information about an extended property.

## Syntax

```
struct ExtendedProperty {
  BSTR PropertyName;
  BSTR PropertyValue;
};
```

## Members

`PropertyName`

Type: **BSTR**

A localized string that contains the name of the extended property.

`PropertyValue`

Type: **BSTR**

A string that represents the value of the extended property. This string should be localized, if appropriate.

## Remarks

This structure is used by the [IUIAutomationStylesPattern::GetCachedExtendedPropertiesArray](/en-us/previous-versions/windows/desktop/legacy/hh437294(v=vs.85)) and [GetCurrentExtendedPropertiesArray](/en-us/previous-versions/windows/desktop/legacy/hh437295(v=vs.85)) methods.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 8 [desktop apps only] |
| **Minimum supported server** | Windows Server 2012 [desktop apps only] |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

---
