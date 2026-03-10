# UiaRaiseActiveTextPositionChangedEvent

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcoreapi/nf-uiautomationcoreapi-uiaraiseactivetextpositionchangedevent)

# UiaRaiseActiveTextPositionChangedEvent function (uiautomationcoreapi.h)

Called by a provider to notify the Microsoft UI Automation core that the position within a text control has programmatically changed.

## Syntax

```
HRESULT UiaRaiseActiveTextPositionChangedEvent(
  [in]           IRawElementProviderSimple *provider,
  [in, optional] ITextRangeProvider        *textRange
);
```

## Parameters

`[in] provider`

Type: **[IRawElementProviderSimple](/en-us/windows/win32/api/uiautomationcore/nn-uiautomationcore-irawelementprovidersimple)\***

The provider node where the position change within the text occurred.

`[in, optional] textRange`

Type: **[ITextRangeProvider](/en-us/windows/win32/api/uiautomationcore/nn-uiautomationcore-itextrangeprovider)\***

The text range change that occurred, if applicable.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this function succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

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

[IUIAutomation6::AddActiveTextPositionChangedEventHandler](../uiautomationclient/nf-uiautomationclient-iuiautomation6-addactivetextpositionchangedeventhandler), [IUIAutomation6::RemoveActiveTextPositionChangedEventHandler](../uiautomationclient/nf-uiautomationclient-iuiautomation6-removeactivetextpositionchangedeventhandler), [IUIAutomationEventHandlerGroup::AddActiveTextPositionChangedEventHandler](../uiautomationclient/nf-uiautomationclient-iuiautomationeventhandlergroup-addactivetextpositionchangedeventhandler)

---
