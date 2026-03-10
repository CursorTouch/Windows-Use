# UiaRaiseTextEditTextChangedEvent

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/nf-uiautomationcoreapi-uiaraisetextedittextchangedevent)

# UiaRaiseTextEditTextChangedEvent function (uiautomationcoreapi.h)

Called by a provider to notify the Microsoft UI Automation core that a text control has programmatically changed text.

## Syntax

```
HRESULT UiaRaiseTextEditTextChangedEvent(
  [in] IRawElementProviderSimple *pProvider,
  [in] TextEditChangeType        textEditChangeType,
  [in] SAFEARRAY                 *pChangedData
);
```

## Parameters

`[in] pProvider`

Type: **[IRawElementProviderSimple](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-irawelementprovidersimple)\***

The provider node where the text change occurred.

`[in] textEditChangeType`

Type: **[TextEditChangeType](/en-us/windows/desktop/api/uiautomationcore/ne-uiautomationcore-texteditchangetype)**

The type of text-edit change that occurred.

`[in] pChangedData`

Type: **[SAFEARRAY](/en-us/windows/desktop/WinAuto/uiauto-workingwithsafearrays)\***

The event data. Should be assignable as a **VAR** of type **VT\_BSTR**.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this function succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

This is a helper function for providers that implement [ITextEditProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-itexteditprovider) and are raising the pattern's required events. Follow the guidance given in [TextEdit Control Pattern](/en-us/windows/desktop/WinAuto/textedit-control-pattern) that describes when to raise the events and what payload the events should pass to UI Automation.

If there are no clients listening for a particular change type, no event is raised.

The event data should contain different payloads for each change type (per [TextEditChangeType](/en-us/windows/desktop/api/uiautomationcore/ne-uiautomationcore-texteditchangetype)):

* **TextEditChangeType\_AutoCorrect**: *pChangedData* should be the new corrected string .
* **TextEditChangeType\_Composition**: *pChangedData* should be the updated string in the composition (only the part that changed).
* **TextEditChangeType\_CompositionFinalized**: *pChangedData* should be the finalized string of the completed composition (this may be empty if composition was canceled or deleted).

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 8.1 [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2012 R2 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcoreapi.h |
| **Library** | Uiautomationcore.lib |
| **DLL** | Uiautomationcore.dll |

## See also

[HandleTextEditTextChangedEvent](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationtextedittextchangedeventhandler-handletextedittextchangedevent)

[ITextEditProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-itexteditprovider)

[IUIAutomation3::AddTextEditTextChangedEventHandler](/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomation3-addtextedittextchangedeventhandler)

[TextEdit Control Pattern](/en-us/windows/desktop/WinAuto/textedit-control-pattern)

---
