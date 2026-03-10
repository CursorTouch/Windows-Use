# HandleTextEditTextChangedEvent

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationclient/nf-uiautomationclient-iuiautomationtextedittextchangedeventhandler-handletextedittextchangedevent)

# IUIAutomationTextEditTextChangedEventHandler::HandleTextEditTextChangedEvent method (uiautomationclient.h)

Handles an event that is raised when a Microsoft UI Automation provider for a text-edit control reports a programmatic text change.

## Syntax

```
HRESULT HandleTextEditTextChangedEvent(
  [in] IUIAutomationElement *sender,
  [in] TextEditChangeType   textEditChangeType,
  [in] SAFEARRAY            *eventStrings
);
```

## Parameters

`[in] sender`

Type: **[IUIAutomationElement](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationelement)\***

A pointer to the element that raised the event.

`[in] textEditChangeType`

Type: **[TextEditChangeType](/en-us/windows/desktop/api/uiautomationcore/ne-uiautomationcore-texteditchangetype)**

The type of text-edit change that occurred.

`[in] eventStrings`

Type: **[SAFEARRAY](/en-us/windows/desktop/WinAuto/uiauto-workingwithsafearrays)\***

Event data passed by the event.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

This method is implemented by the application to handle events that it has subscribed to by using **AddTextEditTextChangedEventHandler**.

The event data contains different payloads for each text-edit change type:

* **TextEditChangeType\_AutoCorrect**: Data is the new corrected string .
* **TextEditChangeType\_Composition**: Data is the updated string in the composition (only the part that changed).
* **TextEditChangeType\_CompositionFinalized**: Data is the finalized string of the completed composition (this may be empty if composition was canceled or deleted).

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 8.1 [desktop apps only] |
| **Minimum supported server** | Windows Server 2012 R2 [desktop apps only] |
| **Target Platform** | Windows |
| **Header** | uiautomationclient.h (include UIAutomation.h) |

## See also

[Best Practices for Using Safe Arrays](/en-us/windows/desktop/WinAuto/uiauto-workingwithsafearrays)

[IUIAutomationTextEditTextChangedEventHandler](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationtextedittextchangedeventhandler)

---
