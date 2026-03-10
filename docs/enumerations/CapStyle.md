# CapStyle

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/ne-uiautomationcore-capstyle)

# CapStyle enumeration (uiautomationcore.h)

Contains values that specify the value of the CapStyle text attribute.

## Syntax

```
typedef enum CapStyle {
  CapStyle_None = 0,
  CapStyle_SmallCap = 1,
  CapStyle_AllCap = 2,
  CapStyle_AllPetiteCaps = 3,
  CapStyle_PetiteCaps = 4,
  CapStyle_Unicase = 5,
  CapStyle_Titling = 6,
  CapStyle_Other = -1
} ;
```

## Constants

|  |
| --- |
| `CapStyle_None` Value: *0* None. |
| `CapStyle_SmallCap` Value: *1* Small capitals. |
| `CapStyle_AllCap` Value: *2* All capitals. |
| `CapStyle_AllPetiteCaps` Value: *3* All petite capitals. |
| `CapStyle_PetiteCaps` Value: *4* Petite capitals. |
| `CapStyle_Unicase` Value: *5* Single case. |
| `CapStyle_Titling` Value: *6* Title case. |
| `CapStyle_Other` Value: *-1* |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps only] |
| **Minimum supported server** | Windows Server 2003 [desktop apps only] |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[Text Attribute Identifiers](/en-us/windows/desktop/WinAuto/uiauto-textattribute-ids)

---
