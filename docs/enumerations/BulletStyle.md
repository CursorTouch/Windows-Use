# BulletStyle

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/ne-uiautomationcore-bulletstyle)

# BulletStyle enumeration (uiautomationcore.h)

Contains values for the BulletStyle text attribute.

## Syntax

```
typedef enum BulletStyle {
  BulletStyle_None = 0,
  BulletStyle_HollowRoundBullet = 1,
  BulletStyle_FilledRoundBullet = 2,
  BulletStyle_HollowSquareBullet = 3,
  BulletStyle_FilledSquareBullet = 4,
  BulletStyle_DashBullet = 5,
  BulletStyle_Other = -1
} ;
```

## Constants

|  |
| --- |
| `BulletStyle_None` Value: *0* None. |
| `BulletStyle_HollowRoundBullet` Value: *1* Hollow round bullet. |
| `BulletStyle_FilledRoundBullet` Value: *2* Filled round bullet. |
| `BulletStyle_HollowSquareBullet` Value: *3* Hollow square bullet. |
| `BulletStyle_FilledSquareBullet` Value: *4* Filled square bullet. |
| `BulletStyle_DashBullet` Value: *5* Dash bullet. |
| `BulletStyle_Other` Value: *-1* Other. |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps only] |
| **Minimum supported server** | Windows Server 2003 [desktop apps only] |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[Text Attribute Identifiers](/en-us/windows/desktop/WinAuto/uiauto-textattribute-ids)

---
