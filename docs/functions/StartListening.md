# StartListening

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nf-uiautomationcore-isynchronizedinputprovider-startlistening)

# ISynchronizedInputProvider::StartListening method (uiautomationcore.h)

Starts listening for input of the specified type.

## Syntax

```
HRESULT StartListening(
  [in] SynchronizedInputType inputType
);
```

## Parameters

`[in] inputType`

Type: **[SynchronizedInputType](/en-us/windows/desktop/api/uiautomationcore/ne-uiautomationcore-synchronizedinputtype)**

The type of input that is requested to be synchronized.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Remarks

When it finds matching input, the provider checks if the target UI Automation element matches the current element. If they match, the provider raises the [UIA\_InputReachedTargetEventId](/en-us/windows/desktop/WinAuto/uiauto-event-ids) event; otherwise, it raises the [UIA\_InputReachedOtherElementEventId](/en-us/windows/desktop/WinAuto/uiauto-event-ids) or [UIA\_InputDiscardedEventId](/en-us/windows/desktop/WinAuto/uiauto-event-ids) event. The UI Automation provider must discard the input if it is for an element other than this one.

This is a one-shot method; after receiving input, the provider stops listening and continues normally.

This method returns E\_INVALIDOPERATION if the provider is already listening for input.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[ISynchronizedInputProvider](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-isynchronizedinputprovider)

---
