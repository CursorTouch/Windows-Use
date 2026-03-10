# SayAsInterpretAs

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/ne-uiautomationcore-sayasinterpretas)

# SayAsInterpretAs enumeration (uiautomationcore.h)

Defines the values that indicate how a text-to-speech engine should interpret specific data.

## Syntax

```
typedef enum SayAsInterpretAs {
  SayAsInterpretAs_None = 0,
  SayAsInterpretAs_Spell = 1,
  SayAsInterpretAs_Cardinal = 2,
  SayAsInterpretAs_Ordinal = 3,
  SayAsInterpretAs_Number = 4,
  SayAsInterpretAs_Date = 5,
  SayAsInterpretAs_Time = 6,
  SayAsInterpretAs_Telephone = 7,
  SayAsInterpretAs_Currency = 8,
  SayAsInterpretAs_Net = 9,
  SayAsInterpretAs_Url = 10,
  SayAsInterpretAs_Address = 11,
  SayAsInterpretAs_Alphanumeric = 12,
  SayAsInterpretAs_Name = 13,
  SayAsInterpretAs_Media = 14,
  SayAsInterpretAs_Date_MonthDayYear = 15,
  SayAsInterpretAs_Date_DayMonthYear = 16,
  SayAsInterpretAs_Date_YearMonthDay = 17,
  SayAsInterpretAs_Date_YearMonth = 18,
  SayAsInterpretAs_Date_MonthYear = 19,
  SayAsInterpretAs_Date_DayMonth = 20,
  SayAsInterpretAs_Date_MonthDay = 21,
  SayAsInterpretAs_Date_Year = 22,
  SayAsInterpretAs_Time_HoursMinutesSeconds12 = 23,
  SayAsInterpretAs_Time_HoursMinutes12 = 24,
  SayAsInterpretAs_Time_HoursMinutesSeconds24 = 25,
  SayAsInterpretAs_Time_HoursMinutes24 = 26
} ;
```

## Constants

|  |
| --- |
| `SayAsInterpretAs_None` Value: *0* The text should be spoken using the default for the text-to-speech engine. |
| `SayAsInterpretAs_Spell` Value: *1* The text should be spoken character by character. |
| `SayAsInterpretAs_Cardinal` Value: *2* The text is an integral or decimal number and should be spoken as a cardinal number. |
| `SayAsInterpretAs_Ordinal` Value: *3* The text is an integral number and should be spoken as an ordinal number. |
| `SayAsInterpretAs_Number` Value: *4* The text should be spoken as a number. |
| `SayAsInterpretAs_Date` Value: *5* The text should be spoken as a date. |
| `SayAsInterpretAs_Time` Value: *6* The text should be spoken as a time value. |
| `SayAsInterpretAs_Telephone` Value: *7* The text should be spoken as a telephone number. |
| `SayAsInterpretAs_Currency` Value: *8* The text should be spoken as currency. |
| `SayAsInterpretAs_Net` Value: *9* The text should be spoken as a network address, including saying the '', '/', and '@' characters. |
| `SayAsInterpretAs_Url` Value: *10* The text should be spoken as a URL. |
| `SayAsInterpretAs_Address` Value: *11* The text should be spoken as an address. |
| `SayAsInterpretAs_Alphanumeric` Value: *12* The text should be spoken as an alphanumeric number. |
| `SayAsInterpretAs_Name` Value: *13* The text should be spoken as a name. |
| `SayAsInterpretAs_Media` Value: *14* The text should be spoken as media. |
| `SayAsInterpretAs_Date_MonthDayYear` Value: *15* The text should be spoken as a date in a Month/Day/Year format. |
| `SayAsInterpretAs_Date_DayMonthYear` Value: *16* The text should be spoken as a date in a Day/Month/Year format. |
| `SayAsInterpretAs_Date_YearMonthDay` Value: *17* The text should be spoken as a date in a Year/Month/Day format. |
| `SayAsInterpretAs_Date_YearMonth` Value: *18* The text should be spoken as a date in a Year/Month format. |
| `SayAsInterpretAs_Date_MonthYear` Value: *19* The text should be spoken as a date in a Month/Year format. |
| `SayAsInterpretAs_Date_DayMonth` Value: *20* The text should be spoken as a date in a Day/Month format. |
| `SayAsInterpretAs_Date_MonthDay` Value: *21* The text should be spoken as a date in a Month/Day format. |
| `SayAsInterpretAs_Date_Year` Value: *22* The text should be spoken as a date in a Year format. |
| `SayAsInterpretAs_Time_HoursMinutesSeconds12` Value: *23* The text should be spoken as a time value in an Hours:Minutes:Seconds 12-hour format. |
| `SayAsInterpretAs_Time_HoursMinutes12` Value: *24* The text should be spoken as a time value in an Hours:Minutes 12-hour format. |
| `SayAsInterpretAs_Time_HoursMinutesSeconds24` Value: *25* The text should be spoken as a time value in an Hours:Minutes:Seconds 24-hour format. |
| `SayAsInterpretAs_Time_HoursMinutes24` Value: *26* The text should be spoken as a time value in an Hours:Minutes 24-hour format. |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 10, version 1703 [desktop apps only] |
| **Minimum supported server** | Windows Server 2016 [desktop apps only] |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

---
