# AddStructureChangedEvent

[Original Documentation](https://learn.microsoft.com/en-us/windows/win32/api/uiautomationcore/nf-uiautomationcore-iproxyproviderwineventsink-addstructurechangedevent)

# IProxyProviderWinEventSink::AddStructureChangedEvent method (uiautomationcore.h)

Raises an event to notify clients that the structure of the UI Automation tree has changed.

## Syntax

```
HRESULT AddStructureChangedEvent(
  [in] IRawElementProviderSimple *pProvider,
  [in] StructureChangeType       structureChangeType,
  [in] SAFEARRAY                 *runtimeId
);
```

## Parameters

`[in] pProvider`

Type: **[IRawElementProviderSimple](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-irawelementprovidersimple)\***

A pointer to the provider of the element that is raising the event.

`[in] structureChangeType`

Type: **[StructureChangeType](/en-us/windows/desktop/api/uiautomationcore/ne-uiautomationcore-structurechangetype)**

The type of structure change that occurred.

`[in] runtimeId`

Type: **[SAFEARRAY](/en-us/windows/win32/api/oaidl/ns-oaidl-safearray)\***

A pointer to the runtime identifiers of the elements that are affected. These IDs enable applications to identify elements that have been removed and are no longer represented by [IUIAutomationElement](/en-us/windows/desktop/api/uiautomationclient/nn-uiautomationclient-iuiautomationelement) interfaces.

## Return value

Type: **[HRESULT](/en-us/windows/desktop/WinProg/windows-data-types)**

If this method succeeds, it returns **S\_OK**. Otherwise, it returns an **HRESULT** error code.

## Requirements

| Requirement | Value |
| --- | --- |
| **Minimum supported client** | Windows 7, Windows Vista with SP2 and Platform Update for Windows Vista, Windows XP with SP3 and Platform Update for Windows Vista [desktop apps | UWP apps] |
| **Minimum supported server** | Windows Server 2008 R2, Windows Server 2008 with SP2 and Platform Update for Windows Server 2008, Windows Server 2003 with SP2 and Platform Update for Windows Server 2008 [desktop apps | UWP apps] |
| **Target Platform** | Windows |
| **Header** | uiautomationcore.h (include UIAutomation.h) |

## See also

[Best Practices for Using Safe Arrays](/en-us/windows/desktop/WinAuto/uiauto-workingwithsafearrays)

**Conceptual**

[IProxyProviderWinEventSink](/en-us/windows/desktop/api/uiautomationcore/nn-uiautomationcore-iproxyproviderwineventsink)

**Reference**

---
