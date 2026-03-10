# ToggleState

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/ne-uiautomationcore-togglestate)

# ToggleState enumeration (uiautomationcore.h)

Contains values that specify the toggle state of a Microsoft UI Automation element that implements the
[Toggle](/en-us/windows/desktop/WinAuto/uiauto-implementingtoggle) *control pattern*.

## Syntax

```
typedef enum ToggleState {
  ToggleState_Off = 0,
  ToggleState_On = 1,
  ToggleState_Indeterminate = 2
} ;
```

## Constants

|  |
| --- |
| `ToggleState_Off` Value: *0* The UI Automation element is not selected, checked, marked or otherwise activated. |
| `ToggleState_On` Value: *1* The UI Automation element is selected, checked, marked or otherwise activated. |
| `ToggleState_Indeterminate` Value: *2* The UI Automation element is in an indeterminate state.     The Indeterminate property can be used to indicate whether the user has acted   on a control. For example, a check box can appear checked and dimmed, indicating an indeterminate state.    Creating an indeterminate state is different from disabling the control.   Consequently, a check box in the indeterminate state can still receive the focus.   When the user clicks an indeterminate control the ToggleState cycles to its next value. |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows XP [desktop apps only] |
| **Minimum supported server** | Windows Server 2003 [desktop apps only] |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[Toggle](/en-us/windows/desktop/api/uiautomationcore/nf-uiautomationcore-itoggleprovider-toggle)

---
