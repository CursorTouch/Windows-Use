# get_StyleId

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nf-uiautomationcore-istylesprovider-get_styleid)

# IStylesProvider::get\_StyleId method (uiautomationcore.h)

Identifies the visual style of an element in a document.

This property is read-only.

## Syntax

```
HRESULT get_StyleId(
  int *retVal
);
```

## Parameters

`retVal`

## Return value

None

## Remarks

A provider should use this property to expose style identifiers that are useful to client applications. For example, a provider might expose the [StyleId\_Title](/en-us/windows/desktop/WinAuto/uiauto-style-identifiers) identifier for an element that represents the title of a presentation. A screen reader could then retrieve the **StyleId** property, discover that the element is a presentation title, and read the title to the user.

### List Styles

IDs for list styles are supported starting with Windows 8.1.

These styles should be applied at a paragraph level; all text that is part of a list item should have one of these styles applied to it.

When bullet styles are mixed within a list, the **BulletedList** style should be applied to the whole range, and the [BulletStyle](/en-us/windows/desktop/api/uiautomationcore/ne-uiautomationcore-bulletstyle) attribute value (property identified by **UIA\_BulletStyleAttributeId**) should be mixed according to breakdown of different bullet types within the range.

When nested lists contain bullets also (perhaps of a different type than the main list), the **BulletedList** style would again be applied to the whole range, and the **BulletStyle** attribute value is whatever the nested bullet style is (for the range covering the nested list).

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 8 [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2012 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[BulletStyle](/en-us/windows/desktop/api/uiautomationcore/ne-uiautomationcore-bulletstyle)

[IStylesProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-istylesprovider)

[UI Automation Support for Textual Content](/en-us/windows/desktop/WinAuto/uiauto-ui-automation-textpattern-overview)

---
