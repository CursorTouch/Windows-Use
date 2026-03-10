# RowOrColumnMajor

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/ne-uiautomationcore-roworcolumnmajor)

# RowOrColumnMajor enumeration (uiautomationcore.h)

Contains values that specify whether data in a table should be read primarily by row or by column.

## Syntax

```
typedef enum RowOrColumnMajor {
  RowOrColumnMajor_RowMajor = 0,
  RowOrColumnMajor_ColumnMajor = 1,
  RowOrColumnMajor_Indeterminate = 2
} ;
```

## Constants

|  |
| --- |
| `RowOrColumnMajor_RowMajor` Value: *0* Data in the table should be read row by row. |
| `RowOrColumnMajor_ColumnMajor` Value: *1* Data in the table should be read column by column. |
| `RowOrColumnMajor_Indeterminate` Value: *2* The best way to present the data is indeterminate. |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps only] |
| **Minimum supported server** | Windows Server 2003 [desktop apps only] |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[Text Attribute Identifiers](/en-us/windows/desktop/WinAuto/uiauto-textattribute-ids)

---
