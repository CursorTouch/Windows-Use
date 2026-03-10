# TextEditChangeType

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/ne-uiautomationcore-texteditchangetype)

# TextEditChangeType enumeration (uiautomationcore.h)

Describes the text editing change being performed by controls when text-edit events are raised or handled.

## Syntax

```
typedef enum TextEditChangeType {
  TextEditChangeType_None = 0,
  TextEditChangeType_AutoCorrect = 1,
  TextEditChangeType_Composition = 2,
  TextEditChangeType_CompositionFinalized = 3,
  TextEditChangeType_AutoComplete = 4
} ;
```

## Constants

|  |
| --- |
| `TextEditChangeType_None` Value: *0* Not related to a specific change type. |
| `TextEditChangeType_AutoCorrect` Value: *1* Change is from an auto-correct action performed by a control. |
| `TextEditChangeType_Composition` Value: *2* Change is from an IME active composition within a control. |
| `TextEditChangeType_CompositionFinalized` Value: *3* Change is from an IME composition going from active to finalized state within a control.   **Note**  The finalized string may be empty if composition was canceled or deleted. |
| `TextEditChangeType_AutoComplete` Value: *4* |

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 8.1 [desktop apps only] |
| **Minimum supported server** | Windows Server 2012 R2 [desktop apps only] |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[ITextEditProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-itexteditprovider)

[Text Attribute Identifiers](/en-us/windows/desktop/WinAuto/uiauto-textattribute-ids)

[UiaRaiseTextEditTextChangedEvent function](/en-us/windows/desktop/api/uiautomationcoreapi/nf-uiautomationcoreapi-uiaraisetextedittextchangedevent)

---
