# TreeScope

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/ne-uiautomationcoreapi-treescope)

# TreeScope enumeration (uiautomationcoreapi.h)

Contains values that specify the scope of various operations in the Microsoft UI Automation tree.

## Syntax

```
typedef enum TreeScope {
  TreeScope_None = 0x0,
  TreeScope_Element = 0x1,
  TreeScope_Children = 0x2,
  TreeScope_Descendants = 0x4,
  TreeScope_Parent = 0x8,
  TreeScope_Ancestors = 0x10,
  TreeScope_Subtree
} ;
```

## Constants

|  |
| --- |
| `TreeScope_None` Value: *0x0* The scope excludes the subtree from the search. |
| `TreeScope_Element` Value: *0x1* The scope includes the element itself. |
| `TreeScope_Children` Value: *0x2* The scope includes children of the element. |
| `TreeScope_Descendants` Value: *0x4* The scope includes children and more distant descendants of the element. |
| `TreeScope_Parent` Value: *0x8* The scope includes the parent of the element. |
| `TreeScope_Ancestors` Value: *0x10* The scope includes the parent and more distant ancestors of the element. |
| `TreeScope_Subtree` The scope includes the element and all its descendants. This flag is a combination of the TreeScope\_Element and TreeScope\_Descendants values. |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps only] |
| **Minimum supported server** | Windows Server 2003 [desktop apps only] |
| **Header** | uiautomationcoreapi.h (include UIAutomation.h, Uiautomationcoreapi.h) |

## See also

[AddAutomationEventHandler](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomation-addautomationeventhandler)

[AddPropertyChangedEventHandler](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomation-addpropertychangedeventhandler)

[AddPropertyChangedEventHandlerNativeArray](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomation-addpropertychangedeventhandlernativearray)

[AddStructureChangedEventHandler](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomation-addstructurechangedeventhandler)

[FindAll](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-findall)

[FindAllBuildCache](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-findallbuildcache)

[FindFirst](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-findfirst)

[FindFirstBuildCache](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-findfirstbuildcache)

**Reference**

---
